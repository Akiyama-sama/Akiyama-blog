---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - React
---

**一、 Jest 基本知识 (Basic Knowledge)**

1. **是什么?**
    
    - Jest 是一个由 Facebook (Meta) 开发并开源的 JavaScript 测试框架。它以“零配置”开箱即用（对很多项目而言）和良好的开发者体验而闻名。
    - 它被广泛用于测试各种 JavaScript 应用，尤其是在 React、React Native、Node.js、TypeScript 等环境中。
2. **核心特点:**
    
    - **内置功能丰富:** Jest 自带了测试运行器 (Test Runner)、断言库 (Assertion Library - 即 `expect` API 和各种 Matchers)、Mocking (模拟) 功能、代码覆盖率报告生成等，通常不需要额外安装很多辅助库。
    - **易于上手:** 设计哲学注重简单性，很多项目可以做到开箱即用或只需少量配置。
    - **测试隔离与并行:** 默认情况下，Jest 会在独立的进程中并行运行测试文件，以提高速度并确保测试之间的隔离。
    - **快照测试 (Snapshot Testing):** 可以方便地对 UI 组件或大型对象进行快照测试，捕捉意外的更改。
    - **强大的 Mocking 系统:** 轻松模拟函数、模块或计时器，以便隔离被测试的单元。
    - **代码覆盖率:** 内置支持生成代码覆盖率报告，帮助了解测试覆盖到了哪些代码。

**二、 Jest 基础用法 (Basic Usage)**

1. **安装:**
    
    - 通常作为开发依赖项安装：Bash
        
        ```
        npm install --save-dev jest
        # 或者
        yarn add --dev jest
        # 或者
        pnpm add --save-dev jest
        ```
        
    - 对于 TypeScript 项目，还需要安装 `ts-jest` 和类型定义：Bash
        
        ```
        npm install --save-dev jest ts-jest @types/jest @jest/globals
        ```
        并在 `jest.config.mjs` (或 `.js`, `.cjs`) 中配置 `preset: 'ts-jest'`。
2. **编写测试文件:**
    
    - **命名约定:** 测试文件通常放在 `__tests__` 目录下，或者与被测试文件放在一起，并使用 `.test.js` (或 `.spec.js`, `.test.ts`, `.spec.ts`) 的后缀。
    - **基本结构:**JavaScript
        
        ```
        // 导入需要测试的模块 (例如 a sum.js 文件)
        // const sum = require('./sum'); // CommonJS
        import { sum } from './sum'; // ES Module / TypeScript
        
        // describe 用于将相关的测试分组，是可选的但推荐使用
        describe('sum module', () => {
        
          // test 或 it 定义一个单独的测试用例
          test('adds 1 + 2 to equal 3', () => {
            // expect 用于包裹要测试的值或函数调用结果
            // .toBe 是一个 Matcher (断言匹配器)，用于检查严格相等 (===)
            expect(sum(1, 2)).toBe(3);
          });
        
          it('adds -1 + 5 to equal 4', () => {
            expect(sum(-1, 5)).toBe(4);
            // 可以有多个 expect 在同一个 test 中
            expect(sum(-1, 5)).not.toBe(0); // .not 用于否定断言
          });
        
        });
        
        // 也可以在没有 describe 的情况下直接写 test
        test('object assignment', () => {
          const data = { one: 1 };
          data['two'] = 2;
          // .toEqual 用于递归比较对象或数组的所有字段 (深度相等)
          expect(data).toEqual({ one: 1, two: 2 });
        });
        ```
        
3. **运行测试:**
    
    - **通过 npm/yarn/pnpm 脚本:** 在 `package.json` 的 `scripts` 中添加 `"test": "jest"`，然后运行 `npm test`, `yarn test` 或 `pnpm test`。
    - **直接运行:** `npx jest` (会查找配置文件并运行所有测试)。
    - **运行特定文件:** `npx jest path/to/your.test.js`。
    - **带选项运行:** `npx jest --watch` (监视文件变化自动重跑), `npx jest --coverage` (生成覆盖率报告)。
4. **常用断言匹配器 (Matchers):**
    
    - Jest 的 `expect()` 返回一个“期望对象”，你可以调用各种匹配器方法来进行断言。
    - **相等性:**
        - `.toBe(value)`: 检查是否严格相等 (`===`)，用于原始类型 (number, string, boolean, null, undefined, symbol, bigint)。
        - `.toEqual(value)`: 检查值是否深度相等，用于对象和数组。
    - **真假性:**
        - `.toBeTruthy()`: 检查值在布尔上下文中是否为 `true` (例如，非 0 数字、非空字符串、对象等)。
        - `.toBeFalsy()`: 检查值在布尔上下文中是否为 `false` (例如，`0`, `''`, `null`, `undefined`, `NaN`)。
        - `.toBeNull()`: 检查值是否为 `null`。
        - `.toBeUndefined()`: 检查值是否为 `undefined`。
        - `.toBeDefined()`: 检查值是否不是 `undefined`。
    - **数字:**
        - `.toBeGreaterThan(number)`: 大于。
        - `.toBeGreaterThanOrEqual(number)`: 大于或等于。
        - `.toBeLessThan(number)`: 小于。
        - `.toBeLessThanOrEqual(number)`: 小于或等于。
        - `.toBeCloseTo(number, numDigits?)`: 检查浮点数是否接近（避免精度问题）。
    - **字符串:**
        - `.toMatch(regexp | string)`: 检查字符串是否匹配正则表达式或包含子字符串。
    - **数组/可迭代对象:**
        - `.toContain(item)`: 检查数组或可迭代对象是否包含某个元素。
        - `.toHaveLength(number)`: 检查数组或字符串的长度。
    - **异常:**
        - `.toThrow(error?)`: 检查函数在调用时是否抛出错误。可以检查错误类型或错误消息。
    - **否定断言:** 可以在任何匹配器前加上 `.not` 来进行否定判断，例如 `expect(value).not.toBe(0);`。
5. **测试异步代码:**
    
    - **Promises:** 在测试函数前使用 `async`，在 `expect` 前使用 `await`。可以使用 `.resolves` 和 `.rejects` 匹配器。JavaScript
        
        ```
        test('fetches data successfully', async () => {
          await expect(fetchData()).resolves.toEqual({ data: 'success' });
        });
        test('fetch fails with an error', async () => {
          await expect(fetchDataWithError()).rejects.toThrow('Network error');
        });
        ```
        
    - **Async/Await:** 最常用的方式。JavaScript
        
        ```
        test('async data is correct', async () => {
          const data = await fetchData();
          expect(data).toEqual({ data: 'success' });
        });
        ```
        
    - **Callbacks:** Jest 也支持测试使用回调函数的异步代码（但不推荐，Promise 和 async/await 更现代）。

**三、 核心概念与最佳实践 (Core Concepts & Best Practices)**

6. **Mocking (模拟):**
    
    - **目的:** 隔离被测试单元，替换其依赖项（如 API 调用、数据库访问、其他模块、定时器等），使得测试更专注、更快速、更稳定。
    - **方法:**
        - `jest.fn(implementation?)`: 创建一个最基础的模拟函数。你可以提供一个可选的实现。这个模拟函数会记录调用情况（参数、次数、返回值等）。
        - `jest.mock('module-path', factory?, options?)`: 自动模拟整个模块。可以提供一个工厂函数来自定义模拟实现。
        - `jest.spyOn(object, methodName)`: "监视"一个对象上的现有方法。它会记录调用情况，但默认仍会执行原始实现（可以链式调用 `.mockImplementation()` 等来改变行为）。
    - **断言 Mock 调用:** 使用 `.toHaveBeenCalled()`, `.toHaveBeenCalledTimes(number)`, `.toHaveBeenCalledWith(...args)`, `.toHaveBeenLastCalledWith(...args)` 等匹配器检查模拟函数是否按预期被调用。
    - **控制 Mock 返回值:** `.mockReturnValue(value)`, `.mockReturnValueOnce(value)`, `.mockResolvedValue(value)` (模拟 Promise 成功), `.mockRejectedValue(value)` (模拟 Promise 失败), `.mockImplementation(fn)`, `.mockImplementationOnce(fn)`。
    - **最佳实践:**
        - 只 Mock 必要的依赖，特别是外部依赖或复杂的内部模块。避免过度 Mocking。
        - 在 `beforeEach` 或 `afterEach` 中使用 `jest.clearAllMocks()` 或 `jest.resetAllMocks()` 清除模拟记录，确保测试独立性。
        - 对于模块级的 Mock (`jest.mock`)，如果需要在测试之间重置模块状态，使用 `jest.resetModules()`。
7. **Snapshot Testing (快照测试):**
    
    - **目的:** 用于测试那些输出结构较大或不易手动编写断言的代码，如 React 组件的渲染输出、大型配置对象等。它能确保你的 UI 或数据结构不会意外改变。
    - **工作方式:**
        1. 第一次运行测试时，Jest 会生成一个包含目标值（如组件结构）的快照文件 (`.snap`) 并存储起来。
        2. 后续运行测试时，Jest 会将当前的实际值与存储的快照进行比较。
        3. 如果两者匹配，测试通过。
        4. 如果不匹配，测试失败，Jest 会显示差异。如果这个变更是故意的，你可以运行 `jest -u` (或 `jest --updateSnapshot`) 来更新快照文件。
    - **用法:** `expect(componentOutput).toMatchSnapshot();`
    - **最佳实践:**
        - 快照应保持相对较小且易于审查。
        - 每次更新快照时，仔细检查 diff，确保变更是符合预期的。
        - 不要滥用快照，它不能替代逻辑测试。它主要用于防止回归（意外的变更）。
8. **测试结构与组织 (Best Practices):**
    
    - **AAA 模式 (Arrange, Act, Assert):** 让每个测试都遵循这个清晰的结构：
        - **Arrange (安排):** 设置测试所需的所有前提条件（初始化变量、设置 Mock、准备输入数据）。
        - **Act (执行):** 调用被测试的代码/函数。
        - **Assert (断言):** 使用 `expect` 验证结果是否符合预期。
    - **清晰的描述:** 使用 `describe` 和 `test`/`it` 给出非常具体和描述性的名称，这样当测试失败时，能快速理解是哪个功能或场景出了问题。例如，`describe('login function', () => { it('should return user token on valid credentials', () => {...}); it('should throw error on invalid password', () => {...}); });`
    - **测试独立性:** 每个 `test` 都应该是独立的，不应依赖于其他测试的执行顺序或产生的副作用。使用 `beforeEach` / `afterEach` 来设置和清理每个测试所需的环境。
    - **避免测试中的逻辑:** 测试代码本身应尽可能简单直接，主要包含 Arrange, Act, Assert，避免复杂的条件判断或循环。
    - **测试行为而非实现细节:** 尽量测试函数的公共接口和预期行为，而不是其内部实现方式。这使得测试在代码重构时更加健壮。
    - **快速失败:** 测试应该尽快失败并给出清晰的错误信息。
    - **使用合适的 Matcher:** 选择最能精确表达意图的 Matcher，而不是泛泛的比较，这有助于理解失败原因。
9. **其他:**
    
    - **Setup/Teardown:** `beforeAll`, `afterAll` (在文件/describe 块开始前/结束后运行一次)，`beforeEach`, `afterEach` (在每个 test 前/后运行)。
    - **代码覆盖率:** 使用 `jest --coverage` 命令生成覆盖率报告，了解哪些代码行、分支、函数被测试覆盖到了。目标不应是 100% 覆盖率，而是确保关键逻辑和边界情况被有效测试。

Jest 是一个非常强大且灵活的框架。掌握它的核心概念、匹配器和 Mocking 功能，并遵循良好的测试实践，可以极大地提升你的 JavaScript/TypeScript 项目的质量和可维护性。对于 Nora 项目，理解 Jest 将有助于你阅读和贡献其测试代码。




# reference
