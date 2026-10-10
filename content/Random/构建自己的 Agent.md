---
date: 2026-10-03
tags:
aliases:
---
参考文章： [Claude Code From Scratch](http://diwang.info/claude-code-from-scratch/#/?id=claude-code-from-scratch)

这是一个最典型的 agent loop 循环：

```
我来读取当前目录下的 package.json 文件。 //第一次 response

🛠️ 执行工具: read_file({"filePath":"package.json"}) //后续直接输出 tool_use的json 格式，以调用内置写好的工具，并把工具的结果给推到 messages 里面去

//进入下一个 loop，messages 里面已经有了工具返回的结果，它直接读就行，读完后输出：
已读取完成，当前目录下的 `package.json` 内容如下： 

//最后不会调用工具，直接结束这个 loop
```

```ts
import dotenv from 'dotenv';
import OpenAI from 'openai';
import type { ChatCompletionMessageParam } from 'openai';
import { toolDefinitions ,executeTool} from './tools';


dotenv.config({ path: 'env.conf' });
const BASE_LOCAL_URL = process.env.BASE_LOCAL_URL
const LOCAL_MODEL = process.env.LOCAL_MODEL ?? 'llama3.2'

const BASE_REMOTE_URL = process.env.BASE_REMOTE_URL
const REMOTE_MODEL = process.env.REMOTE_MODEL ?? 'llama3.2'

const BASE_URL = process.env.USAGE === 'REMOTE' ? BASE_REMOTE_URL : BASE_LOCAL_URL
const MODEL = process.env.USAGE === 'REMOTE' ? REMOTE_MODEL : LOCAL_MODEL

const SYSTEM_PROMPTS = '你是一个可以调用工具的大模型'

const apiKey = process.env.API_KEY
const client = new OpenAI({
        baseURL: BASE_URL,
        apiKey: apiKey
});

//主函数
export default async function main(){
    const messages: ChatCompletionMessageParam[] = [{ role: 'user', content: '你来帮我读一下当前目录下的 package.json' }]
    const system = SYSTEM_PROMPTS
    while(true){
        const response =await client.chat.completions.create({
            model:MODEL,
            messages,
            stream:true,
            tools: toolDefinitions,
        })
        
        
        let fullContent = '';
        const toolCalls: any[] = [];

        for await (const chunk of response) {
            const delta = chunk.choices[0]?.delta;

            // 1. 打印模型的思考文本输出
            if (delta?.content) {
                process.stdout.write(delta.content);
                fullContent += delta.content;
            }

            // 2. 收集流式的 Tool Call 碎片
            if (delta?.tool_calls) {
            for (const tc of delta.tool_calls) {
                if (!toolCalls[tc.index]) {
                toolCalls[tc.index] = {
                    id: tc.id,
                    type: 'function',
                    function: { name: tc.function?.name || '', arguments: '' }
                };
                }
                if (tc.function?.arguments) {
                toolCalls[tc.index].function.arguments += tc.function.arguments;
                }
            }
            }
        }
        // 3. 如果模型没有发起 Tool Call，说明工作结束，跳出循环
        if (toolCalls.length === 0) {
            messages.push({ role: 'assistant', content: fullContent });
            console.log('\n\n✅ Agent 完成任务!');
            break;
        }

        // 把助手消息(含 tool_calls)完整写回，tool 结果必须紧随其后
        const normalizedCalls = toolCalls.map((tc, index) => ({
            id: tc.id ?? `call_${index}`,
            type: 'function' as const,
            function: { name: tc.function.name, arguments: tc.function.arguments || '{}' },
        }));
        messages.push({
            role: 'assistant',
            content: fullContent || null,
            tool_calls: normalizedCalls,
        });

        // 4. 执行所有被调用的工具，并将结果写回 messages (role: 'tool')
        for (const toolCall of normalizedCalls) {
            const functionName = toolCall.function.name;
            const functionArgs = JSON.parse(toolCall.function.arguments);
            
            console.log(`\n🛠️ 执行工具: ${functionName}(${JSON.stringify(functionArgs)})`);
            const result = await executeTool(functionName, functionArgs);

            messages.push({
                role: 'tool',
                tool_call_id: toolCall.id,
                content: result,
            });
        }

    }
}
```


上面只有 read_file这一个工具，我们仅需补充 tools 就能够让 Agent 做到更多事情：
```
❯ bun run index.ts
◇ injected env (6) from env.conf

🛠️ 执行工具: read_file({"filePath":"test.txt"})

🛠️ 执行工具: list_files({"path":"."})

🛠️ 执行工具: read_file({"filePath":"README.md"})

🛠️ 执行工具: read_file({"filePath":"CLAUDE.md"})

🛠️ 执行工具: edit_file({"filePath":"test.txt","oldString":"1. 这是第一行\n2. ","newString":"1. 这是第一行\n2. 这是第二行"})

🛠️ 执行工具: read_file({"filePath":"test.txt"})

🛠️ 执行工具: run_shell({"command":"xxd test.txt | tail -3"})

🛠️ 执行工具: run_shell({"command":"printf '\\n' >> test.txt && xxd test.txt | tail -2"})
已读取 `test.txt`，它只有一行内容、第二行是空的（`2. ` 后面没有任何文字）。

我按第一行的句式对称补充了第二行：

1. 这是第一行
2. 这是第二行


另外发现原文件结尾缺少换行符（末行没有 `\n`），已顺手补上，现在文件以换行结尾，符合 POSIX 文本文件惯例。

如果你本意不是补一句占位文本，而是想让第二行承载具体内容（比如接续某个列表、写代码片段、或英文版本 `2. This is the second line`），告诉我具体诉求，我可以立刻改写。

✅ Agent 完成任务!
```

