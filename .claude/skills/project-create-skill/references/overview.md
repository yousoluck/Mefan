# Feature Skill 代码示例

本目录包含 Feature Skill 的代码示例，用于供 Dev Agent 参考实现。

## 目录结构

```
references/
├── entity.ts           # 领域实体示例
├── service.ts          # 应用服务示例
├── repository.ts       # 仓储实现示例
├── controller.ts       # 控制器示例
├── dto.ts              # 数据传输对象示例
└── data-flow.ts        # 数据流示例
```

## 使用说明

Dev Agent 在实现新的 Feature 时，应参考以下示例：

1. **entity.ts** - 参考领域实体的定义方式
2. **service.ts** - 参考应用服务的实现模式
3. **repository.ts** - 参考仓储的实现方式
4. **controller.ts** - 参考接口层的定义
5. **dto.ts** - 参考 DTO 的定义方式
6. **data-flow.ts** - 参考完整的数据流转

## 示例代码

### entity.ts 示例

```typescript
// 领域实体示例
export class User {
  private id: string;
  private email: string;
  private passwordHash: string;
  private status: UserStatus;

  constructor(props: { id: string; email: string; passwordHash: string }) {
    this.id = props.id;
    this.email = props.email;
    this.passwordHash = props.passwordHash;
    this.status = UserStatus.ACTIVE;
  }

  // 领域方法
  public activate(): void {
    this.status = UserStatus.ACTIVE;
  }

  public deactivate(): void {
    this.status = UserStatus.INACTIVE;
  }

  // Getters
  public getId(): string {
    return this.id;
  }

  public getEmail(): string {
    return this.email;
  }

  public getStatus(): UserStatus {
    return this.status;
  }
}

export enum UserStatus {
  ACTIVE = 'ACTIVE',
  INACTIVE = 'INACTIVE',
  SUSPENDED = 'SUSPENDED',
}
```

### service.ts 示例

```typescript
// 应用服务示例
export class UserService {
  constructor(
    private userRepository: UserRepository,
    private passwordEncoder: PasswordEncoder,
    private eventPublisher: EventPublisher
  ) {}

  async createUser(command: CreateUserCommand): Promise<User> {
    // 1. 检查 email 是否已存在
    const existing = await this.userRepository.findByEmail(command.email);
    if (existing) {
      throw new UserAlreadyExistsError(command.email);
    }

    // 2. 密码加密
    const passwordHash = await this.passwordEncoder.encode(command.password);

    // 3. 创建实体
    const user = new User({
      id: generateId(),
      email: command.email,
      passwordHash,
    });

    // 4. 保存
    await this.userRepository.save(user);

    // 5. 发布领域事件
    this.eventPublisher.publish(new UserCreatedEvent(user));

    return user;
  }
}
```
