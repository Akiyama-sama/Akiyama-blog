---
tags:
  - '#pernamant'
  - React
---
## 嵌套列表

```js
import { recipes } from './data.js';

export default function RecipeList() {
  return (
    <div>
      <h1>菜谱</h1>
      {recipes.map(recipe =>
        <div key={recipe.id}>
          <h2>{recipe.name}</h2>
          <ul>
            {recipe.ingredients.map(ingredient =>
              <li key={ingredient}>
                {ingredient}
              </li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}

```
`recipes` 数组中每一项都拥有一个 `id`，所以外层的循环可以直接拿它作为 `key`。不过，在循环遍历原料的时候就没有现成的 `id` 可以用了。但是，合理推测一下，一份菜谱里不会罗列多次同一种原料，所以其实原料的名字就适合作为 `key`。此外，你也可以自行修改原本的数据人为增加一项 `id`，或是使用索引作为 `key`（需要注意的是，这么做会使你无法正常地对原料进行排序）。
## 讲其提取为组件
```js
import { recipes } from './data.js';

function Recipe({ id, name, ingredients }) {
  return (
    <div>
      <h2>{name}</h2>
      <ul>
        {ingredients.map(ingredient =>
          <li key={ingredient}>
            {ingredient}
          </li>
        )}
      </ul>
    </div>
  );
}

export default function RecipeList() {
  return (
    <div>
      <h1>菜谱</h1>
      {recipes.map(recipe =>
        <Recipe {...recipe} key={recipe.id} />
      )}
    </div>
  );
}


```

这里的 `<Recipe {...recipe} key={recipe.id} />` 是一种简写方式，它表示“把 `recipe` 对象里的每个属性都作为 props 传给 `Recipe` 组件”。这和直接写明每一个 prop 是等价的：`<Recipe id={recipe.id} name={recipe.name} ingredients={recipe.ingredients} key={recipe.id} />`。

**注意这里的 `key` 是写在 `<Recipe>` 组件本身上的，不要写在 `Recipe` 内部返回的 `<div>` 上。** 这是因为 `key` 只有在就近的数组上下文中才有意义。之前的写法里，我们生成了一个 `<div>` 的数组所以其中的每一项需要一个 `key`，但是现在的写法里，生成的实际上是 `<Recipe>` 的数组。换句话说，在提取组件的时候，`key` 应该写在复制粘贴的 JSX 的外层组件上。




# reference
