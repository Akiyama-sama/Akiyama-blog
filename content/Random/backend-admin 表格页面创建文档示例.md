---
tags:
  - '#pernamant'
---
## 目录
![file-20250402085119376](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/file-20250402085119376.jpg)
conponents放这个页面相关的组件
context用于创建user的上下文context与封装自定义hook
data存放user数据结构相关的文件

## 准备工作data
schema.ts 用于存放数据模式 Schema 是对数据结构或数据组织方式的描述，定义了数据的格式、字段和关系。而里面的zod依赖是用来检查其类型安全的
```ts schema.ts
import { z } from "zod";
export const UserSchema = z.object({
    id: z.number(),
    userName: z.string(),
    password: z.string(),
    createDate: z.date(),
})
export type User = z.infer<typeof UserSchema>
export const UserListSchema = z.array(UserSchema)
```

user-data-ts 用于存放静态user数据
然后我们需要复制粘贴columns到componts，再自行根据自己的数据结构进行修改，这是data-table所需的一个参数columns，来定义表格的行：
* 可以用复选框多选
* 展示哪些列
* 对某行进行哪些操作
```tsx
import { ColumnDef } from "@tanstack/react-table";
import { Checkbox } from "@/components/ui/checkbox";

import { DataTableRowActions } from "./data-table-row-actions";//这里会爆红，因为没有创建
import { User } from "../data/schema";

export const columns: ColumnDef<User>[] = [
    {
        id: "select",//多选框，详情见shadcnUI文档中的data-table
        header: ({ table }) => (
          <Checkbox
            checked={
              table.getIsAllPageRowsSelected() ||
              (table.getIsSomePageRowsSelected() && "indeterminate")
            }
            onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
            aria-label="Select all"
          />
        ),
        cell: ({ row }) => (
          <Checkbox
            checked={row.getIsSelected()}
            onCheckedChange={(value) => row.toggleSelected(!!value)}
            aria-label="Select row"
          />
        ),
        enableSorting: false,
        enableHiding: false,
      },
      {
        accessorKey: "userName",
        header: "用户名",
      },
      {
        accessorKey: "password",
        header: "密码",
      },
      {
        accessorKey: "createDate",
        header: "创建日期",
        
      },
      {
        id: "actions",//对行进行操作，详情见shadcnUI文档
        cell: ({row}) => {
          return (
            <DataTableRowActions row={row} />
          )
        },
      },
]

```

我们再来粘贴，修改一下data-table-row-actions

```tsx
·······
import { useUser } from '../../users/context/userContext'//这里还需要一个文件
import { User } from '../data/schema'

interface DataTableRowActionsProps {
  row: Row<User>
}

export function DataTableRowActions({ row }: DataTableRowActionsProps) {
  const { setOpen, setCurrentRow } = useUser()
  return (
    <>
     ····
    </>
  )
}

```

再粘贴修改一下userContext.tsx

```tsx
import React, { useState } from 'react'
import useDialogState from '@/hooks/use-dialog-state'
import { User } from '../data/schema'

type UserDialogType = 'create' | 'update' | 'delete'|'import'

interface UserContextType {
  open: UserDialogType | null
  setOpen: (str: UserDialogType | null) => void
  currentRow: User | null
  setCurrentRow: React.Dispatch<React.SetStateAction<User | null>>
}

const UserContext = React.createContext<UserContextType | null>(null)

interface Props {
  children: React.ReactNode
}


export default function UserProvider({ children }: Props) {
  const [open, setOpen] = useDialogState<UserDialogType>(null)
  const [currentRow, setCurrentRow] = useState<User | null>(null)
  
  return (
    <UserContext.Provider value={{ open, setOpen, currentRow, setCurrentRow }}>
      {children}
    </UserContext.Provider>
  )
}

// eslint-disable-next-line react-refresh/only-export-components
export const useUser = () => {
  const userContext = React.useContext(UserContext)

  if (!userContext) {
    throw new Error('useUser has to be used within <UserContext>')
  }

  return userContext
}

```

此时data-table-row-actions不会爆红了

colums这个参数也准备好了

## 入口文件user.tsx
```tsx
export function User() {
    return (
        <UserProvider> //提供UserContext
            <UserHeader />//数据表格之外的部分
            <DataTable columns={columns} data={UserData} />//数据表格的主题部分
            <UserDialog />//根据条件弹出来的对话框
        </UserProvider>

    )

}
```
接下来我们将会一步一步生成这些组件

## user-header
您可以自定义这些header的内容

```tsx
export function UserHeader() {
    return (
        <div>
            <h1 className="text-3xl font-bold mb-6">用户管理</h1>
        </div>
    )
```



## data-table
您可以直接复制粘贴data-table过来，这些是非常典型的组件，您可以从employee这个文件夹中的内容进行复制粘贴

复制到conponents文件夹后会有报错，还有一个组件需要我们创建，这个组件是用于操作表格的工具

./data-table-toolbar,小修一下

```tsx
import { Table } from "@tanstack/react-table"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { DropdownMenu, DropdownMenuContent, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { DropdownMenuCheckboxItem } from "@/components/ui/dropdown-menu"
import { TrashIcon } from "lucide-react"
import { useUser } from "../context/userContext"
interface DataTableToolbarProps<TData> {
  table: Table<TData>
}
export default function DateTableToolbar<TData>({
  table,
}: DataTableToolbarProps<TData>) {
    const {setOpen} = useUser()
  return (
    <div className="flex justify-between py-4">
        <div className="flex items-center space-x-2">
          {/* 搜索框 */}
        <Input
          placeholder="搜索用户..."
          value={(table.getColumn("userName")?.getFilterValue() as string) ?? ""}
          onChange={(event) =>
            table.getColumn("userName")?.setFilterValue(event.target.value)
          }
          className="max-w-sm"
        />
         {/*批量选中时，出现的删除按钮 */}
         {table.getFilteredSelectedRowModel().rows.length>0&&(
          <TrashIcon className="w-4 h-4" onClick={()=>{
            setOpen('delete')
          }}/>
         )}
        </div>
        
        
        <div className="flex items-center space-x-2">
         
          
          {/* 添加订单 */}
          <Button variant="outline" onClick={()=>{
            setOpen('create')
          }}>添加用户</Button>
          {/* 表格列选择 */}

          <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="ml-auto">
              列选择
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            {table
              .getAllColumns()
              .filter(
                (column) => column.getCanHide()
              )
              .map((column) => {
                return (
                  <DropdownMenuCheckboxItem
                    key={column.id}
                    className="capitalize"
                    checked={column.getIsVisible()}
                    onCheckedChange={(value) =>
                      column.toggleVisibility(!!value)
                    }
                  >
                    {column.id}
                  </DropdownMenuCheckboxItem>
                )
              })}
          </DropdownMenuContent>
          </DropdownMenu>
        </div>
        
      </div>
  )
}

```

## 展示一下

在routes/index.tsx修改一下路由

```tsx
import {createBrowserRouter} from 'react-router-dom';
import Order from '../features/manageView/order/order.tsx';
import Index from '../features/app/layout';
import Dashboard from '../features/dashboard/dashboard';
import Employee from '../features/manageView/employee/employee';
import { User } from '../features/manageView/users/user';
export const router =createBrowserRouter([
    {
        path:'/',
        element:<Index/>,
        children:[{
            index:true,
            element:<Dashboard />
        },
        {
            path:'manageView/order',
            element:<Order />
        },
        {
            path:'manageView/employee',
            element:<Employee />
        },
        {
            path:'manageView/users',
            element:<User />
        }
    ]
    },
    
])

```

修改一下siderbar的配置

```JSON
{
          title: 'Users',
          url: '/manageView/users',
          icon: IconUsers,
},
```

![file-20250402100000726](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/file-20250402100000726.jpg)
基本的表格就可以展示出来了

## user-dialog
这个文件是用来根据条件渲染对话框的，例如点击删除会弹出是否确认删除，点击添加会弹出添加的对话框

```tsx
import { toast } from '@/hooks/use-toast'
import { ConfirmDialog } from '@/components/confirm-dialog'
import { useUser } from '../context/userContext'
import { UserMutateDrawer } from './user-mutate-drawer'//会爆红，等会儿创建

export function UserDialogs() {
  const { open, setOpen, currentRow, setCurrentRow } = useUser()
  return (
    <>
      <UserMutateDrawer
        key='user-create'
        open={open === 'create'}
        onOpenChange={() => setOpen('create')}
      />
      
      {currentRow && (//选中当前行后才会根据条件渲染
        <>
          <UserMutateDrawer
            key={`user-update-${currentRow.id}`}
            open={open === 'update'}
            onOpenChange={() => {
              setOpen('update')
              setTimeout(() => {
                setCurrentRow(null)
              }, 500)
            }}
            currentRow={currentRow}
          />

          <ConfirmDialog //当点击当前行删除，才弹出来的确认对话框
            key='user-delete'
            destructive
            open={open === 'delete'}
            onOpenChange={() => {
              setOpen('delete')
              setTimeout(() => {
                setCurrentRow(null)
              }, 500)
            }}
            handleConfirm={() => {
              setOpen(null)
              setTimeout(() => {
                setCurrentRow(null)
              }, 500)
              toast({
                title: 'The following employee has been deleted:',
                description: (
                  <pre className='mt-2 w-[340px] rounded-md bg-slate-950 p-4'>
                    <code className='text-white'>
                      {JSON.stringify(currentRow, null, 2)}
                    </code>
                  </pre>
                ),
              })
            }}
            className='max-w-md'
            title={`Delete this employee: ${currentRow.id} ?`}
            desc={
              <>
                You are about to delete a employee with the ID{' '}
                <strong>{currentRow.id}</strong>. <br />
                This action cannot be undone.
              </>
            }
            confirmText='Delete'
          />
        </>
      )}
    </>
  )
}

```

我们再粘贴修改一下user-mutate-drawer

```tsx
import { z } from 'zod'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { toast } from '@/hooks/use-toast'
import { Button } from '@/components/ui/button'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from '@/components/ui/sheet'
import { User, UserSchema } from '../data/schema'

interface Props {
  open: boolean
  onOpenChange: (open: boolean) => void
  currentRow?: User
}


type UserForm = z.infer<typeof UserSchema>

export function UserMutateDrawer({ open, onOpenChange, currentRow }: Props) {
  const isUpdate = !!currentRow

  const form = useForm<UserForm>({
    resolver: zodResolver(UserSchema),
    defaultValues: currentRow ?? {
      id: 0,
      userName: '',
      password: '',
      createDate: new Date(),
    },
  })

  const onSubmit = (data: UserForm) => {
    // do something with the form data
    onOpenChange(false)
    form.reset()
    toast({
      title: 'You submitted the following values:',
      description: (
        <pre className='mt-2 w-[340px] rounded-md bg-slate-950 p-4'>
          <code className='text-white'>{JSON.stringify(data, null, 2)}</code>
        </pre>
      ),
    })
  }

  return (
    <Sheet
      open={open}
      onOpenChange={(v) => {
        onOpenChange(v)
        form.reset()
      }}
    >
      <SheetContent className='flex flex-col'>
        <SheetHeader className='text-left'>
          <SheetTitle>{isUpdate ? 'Update' : 'Create'} User</SheetTitle>
          <SheetDescription>
            {isUpdate
              ? 'Update the user by providing necessary info.'
              : 'Add a new user by providing necessary info.'}
            Click save when you&apos;re done.
          </SheetDescription>
        </SheetHeader>
        <Form {...form}>
          <form
            id='employee-form'
            onSubmit={form.handleSubmit(onSubmit)}
            className='flex-1 space-y-5'
          >
            <FormField
              control={form.control}
              name='userName'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>用户名</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder='Enter a userName' />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name='password'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>密码</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder='Enter a password' />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
          </form>
        </Form>
        <SheetFooter className='gap-2'>
          <SheetClose asChild>
            <Button variant='outline'>取消</Button>
          </SheetClose>
          <Button form='user-form' type='submit'>
            {isUpdate ? '更新' : '创建'}
          </Button>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  )
}

```

最后再user.tsx入口文件加上<UserDialogs />
![file-20250402101512153](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/file-20250402101512153.jpg)
就可以正常使用了



# reference
