# Before & After: Clean Code Rewrites

Five real-world transformations showing how to apply clean code principles.

---

## Example 1: Monolith Function → Single Responsibility

### Before (83 lines, does 5 things)

```typescript
async function handleUserRegistration(req: Request, res: Response) {
  // Validate input
  if (!req.body.email || !req.body.password || !req.body.name) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(req.body.email)) {
    return res.status(400).json({ error: 'Invalid email' });
  }
  if (req.body.password.length < 8) {
    return res.status(400).json({ error: 'Password too short' });
  }

  // Check if user exists
  const existingUser = await db.query(
    'SELECT id FROM users WHERE email = $1',
    [req.body.email]
  );
  if (existingUser.rows.length > 0) {
    return res.status(409).json({ error: 'Email already registered' });
  }

  // Hash password
  const salt = await bcrypt.genSalt(10);
  const hashedPassword = await bcrypt.hash(req.body.password, salt);

  // Create user
  const newUser = await db.query(
    `INSERT INTO users (name, email, password_hash, created_at)
     VALUES ($1, $2, $3, NOW()) RETURNING id, name, email`,
    [req.body.name, req.body.email, hashedPassword]
  );

  // Send welcome email
  await transporter.sendMail({
    from: 'noreply@app.com',
    to: req.body.email,
    subject: 'Welcome!',
    html: `<h1>Hi ${req.body.name}</h1><p>Thanks for registering!</p>`
  });

  // Generate token
  const token = jwt.sign(
    { userId: newUser.rows[0].id, email: newUser.rows[0].email },
    process.env.JWT_SECRET!,
    { expiresIn: '7d' }
  );

  return res.status(201).json({
    user: { id: newUser.rows[0].id, name: newUser.rows[0].name, email: newUser.rows[0].email },
    token
  });
}
```

### After (5 files, each under 40 lines)

```typescript
// handlers/registrationHandler.ts (16 lines)
async function handleUserRegistration(req: Request, res: Response): Promise<void> {
  const params = validateRegistrationInput(req.body);
  await assertEmailNotTaken(params.email);
  const user = await createUser(params);
  await sendWelcomeEmail(user);
  const token = generateAuthToken(user);
  res.status(201).json({ user, token });
}

// validation/registrationValidator.ts (18 lines)
interface IRegistrationParams {
  name: string;
  email: string;
  password: string;
}
function validateRegistrationInput(body: unknown): IRegistrationParams {
  const { name, email, password } = body as Record<string, string>;
  if (!name || !email || !password) throw new ValidationError('Missing required fields');
  if (!isValidEmail(email)) throw new ValidationError('Invalid email');
  if (password.length < 8) throw new ValidationError('Password must be at least 8 characters');
  return { name, email, password };
}

// repositories/userRepository.ts (interface + implementation)
interface IUserRepository {
  findByEmail(email: string): Promise<User | null>;
  create(params: ICreateUserParams): Promise<User>;
}

// services/authService.ts (token generation)
// services/emailService.ts (welcome email)
```

**Principles applied:** SRP, Extract Function, Interfaces, Parameter Objects

---

## Example 2: Deep Nesting → Guard Clauses

### Before (nesting depth 5)

```typescript
function processPayment(order: any) {
  if (order) {
    if (order.status === 'pending') {
      if (order.items && order.items.length > 0) {
        if (order.customer && order.customer.paymentMethod) {
          if (order.total > 0) {
            // Actual work buried at level 5
            chargeCard(order.customer.paymentMethod, order.total);
            order.status = 'paid';
            return { success: true };
          } else {
            return { error: 'Invalid total' };
          }
        } else {
          return { error: 'No payment method' };
        }
      } else {
        return { error: 'Empty order' };
      }
    } else {
      return { error: 'Order not pending' };
    }
  } else {
    return { error: 'No order' };
  }
}
```

### After (max nesting depth 1)

```typescript
function processPayment(order: IOrder): IPaymentResult {
  if (!order) throw new OrderError('No order provided');
  if (order.status !== 'pending') throw new OrderError('Order not pending');
  if (!order.items?.length) throw new OrderError('Order has no items');
  if (!order.customer?.paymentMethod) throw new PaymentError('No payment method');
  if (order.total <= 0) throw new PaymentError('Invalid total');

  chargeCard(order.customer.paymentMethod, order.total);
  order.status = 'paid';
  return { success: true };
}
```

**Principles applied:** Guard Clauses, Early Return, Intention-Revealing Errors

---

## Example 3: Generic Names → Intention-Revealing Names

### Before

```typescript
function calc(d: any[], n: number): any {
  let r = 0;
  for (let i = 0; i < d.length; i++) {
    if (d[i].t === n) {
      r += d[i].v;
    }
  }
  return r;
}
```

### After

```typescript
function sumTransactionsByType(transactions: ITransaction[], targetType: TransactionType): number {
  return transactions
    .filter(transaction => transaction.type === targetType)
    .reduce((total, transaction) => total + transaction.amount, 0);
}
```

**Principles applied:** Intention-Revealing Names, DRY (reduce replaces manual sum)

---

## Example 4: Missing Interface → Depend on Abstraction

### Before

```typescript
class ReportService {
  constructor(
    private readonly postgres: PostgresDatabase,  // concrete class
    private readonly sendgrid: SendGridMailer,    // concrete class
    private readonly redis: RedisCache            // concrete class
  ) {}

  async generateReport(userId: string): Promise<Report> {
    const data = await this.postgres.query(`SELECT * FROM reports WHERE user_id = $1`, [userId]);
    const cached = await this.redis.get(`report:${userId}`);
    // ...
  }
}
```

### After

```typescript
// Each dependency defined by interface — testable, swappable
interface IDatabase {
  query<T>(sql: string, params?: unknown[]): Promise<T[]>;
}

interface IMailer {
  send(to: string, subject: string, body: string): Promise<void>;
}

interface ICache {
  get(key: string): Promise<string | null>;
  set(key: string, value: string, ttlSeconds?: number): Promise<void>;
}

class ReportService {
  constructor(
    private readonly db: IDatabase,      // inject interface
    private readonly mailer: IMailer,
    private readonly cache: ICache
  ) {}

  async generateReport(userId: string): Promise<Report> {
    const cached = await this.cache.get(`report:${userId}`);
    if (cached) return JSON.parse(cached);

    const data = await this.db.query<ReportRow>('SELECT * FROM reports WHERE user_id = $1', [userId]);
    // ...
  }
}
```

**Principles applied:** Dependency Inversion, Interface Segregation, Testability

---

## Example 5: Long File → Split by Responsibility

### Before

```
// userUtils.ts — 480 lines
// Contains: formatUserName, hashPassword, validateEmail,
//           sendWelcomeEmail, sendPasswordReset,
//           getUserFromDb, saveUserToDb, deleteUser,
//           checkUserPermission, getUserRole
```

### After

```
src/users/
├── formatting/
│   └── userFormatter.ts        (formatUserName, displayName, initials)
├── auth/
│   ├── passwordService.ts      (hashPassword, verifyPassword)
│   └── emailValidator.ts       (validateEmail, isDisposable)
├── email/
│   ├── IEmailService.ts        (interface)
│   └── userEmailService.ts     (sendWelcome, sendPasswordReset)
├── repositories/
│   ├── IUserRepository.ts      (interface)
│   └── userRepository.ts       (get, save, delete — database only)
└── permissions/
    └── userPermissions.ts      (checkPermission, getUserRole)
```

Each file: under 80 lines. Each file does exactly one thing.

**Principles applied:** SRP, File Size, Interface Segregation, DRY (each utility in one place)
