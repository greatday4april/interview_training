# interview_training


# Subarray 问题

## Sliding Window

> Sliding window 通常用于处理subarray / substring 长度确定，或者window长度受到某个因素制约（越扩张越接近条件）的问题。

比如 Longest subarray / Longest substring / pattern match, 用sliding window处理, 并且update global state (max, indices etc)

## Array - Dynamic Programming / 递推问题

求解满足条件，或者最优的subarray / substring / subsequence / pair 的问题，用dynamic programming。也就是观察：如果需要对以idx为结尾的pair或者subarray得出结论，我们需要从前面的循环中获得什么信息呢？(与divide and conquer的思路相似) 然后再尽可能通过每一步cache的方式，使得这个信息能够被高效地得到

*通常可以从idx = 1开始遍历，使得第一个元素直接成为初始值，简化处理*

- e.g. [Maximum Product Array](https://leetcode.com/problems/maximum-product-subarray/)

*与sliding window的显著区别是，当subarray end_idx在expand时，并不能使得左侧start index收缩*

## Array - Intersection / Merge

2个或多个array intersect或merge的问题，每次所有array中头部的最小元素，作为当前的candidate，然后移动对应array的index。

- e.g. [Two Person Meeting Scheduler](https://leetcode.com/problems/meeting-scheduler/)

如果两个array有一个特别短，则对短array循环，对长array做binary search查找对应元素
- e.g. [Sparse Vector Dot](https://leetcode.com/discuss/interview-question/124823/dot-product-of-sparse-vector)

对于k个array的情况，用heap作为缓存来求当前的最小元素。
- e.g. [Merge K sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)
- e.g. [Sorted Iterator Over K Sorted Lists](https://leetcode.com/discuss/interview-question/169334/facebook-phone-screen-sorted-iterator)

## Event / Interval

- 求两个interval的overlap或merge

```Ruby
low_a, high_a = intervals_a[idx_a]
low_b, high_b = intervals_b[idx_b]

# overlap
low = [low_a, low_b].max
high = [high_a, high_b].min

# merge (assume a.start < b.start) 和overlap反过来
if low_b <= high_a  # has overlap
  low = [low_a, low_b].min
  high = [high_a, high_b].max
end
```

- 一个list内merge interval的问题，用sliding window，然后试图求`window`与当前interval的overlap，当没有overlap时switch window。

  - e.g. [Insert Interval](https://leetcode.com/problems/insert-interval/)

- 对两个list求interval intersection的问题，用array - intersection的方法，当两者有overlap时添加这个intersection，然后根据两个interval的high来选择哪个list前进

- 更复杂的问题例如有两人以上或者求满足特定条件的interval问题，统一用`Event`来表示interval的开始和结束，然后sort所有的event依次用sliding window处理，当计数由0变正数时就是window的开始，由正数变0时就是window的结束。
    - e.g. [Meeting Rooms II]
    - 如果在同一时间可能发生多个事件并且可能有冲突，那么应该按照时间对event归类然后再对这些时间bucket进行sort，每次处理一个bucket而非一个event
      - e.g. [Skyline Problem]

## Optimal Path - Memoization

- 如果是最短路径或者最小数量优先考虑用BFS. 如果是从任何点到达某个点或任何点，可以将所有出发点都放入queue然后进行BFS
  - e.g. [Jump Game II]
  - e.g. [Perfect Squares]
- 注意所有变动参数必须作为memoization的function param, 所以memoization不能使用变动的全局变量，而需要记录visiting的问题无法使用memoization
- 对于coin change或者perfect squares这一类可以重复使用的，优先每次尝试所有选择的办法，这样可以节省空间复杂度

## Backtracking

- 在递归的每一层 需要跳过重复的选择 但是不影响下一层

  - e.g. [Combination Sum II](https://leetcode.com/problems/combination-sum-ii/)

## Graph

### 无向图 Connected Component 问题: Graph => 多个part (array of array)

给出相互之间的联系，把元素归类起来的问题：

可以循环所有点出发DFS，用@visiting记录访问过的点 (注意@visiting在DFS时不需要revert)，这些点就是connected component。用ordered set @visited记录所有访问过的点

**connected component关注的是每一个section的访问痕迹，也就是`@visiting`**

```Ruby
def traverse()
  @visited = Set.new
  (0...matrix.length).each do |i|
    (0...matrix[0].length).each do |j|
      next if @visited.include?([i, j])
      @visiting = Set.new
      traverse_from([i, j])
      # here we have @visiting as connected components
    end
  end
end

def traverse_from(cell)
  return if @visiting.include?(cell)

  @visiting.add(cell)
  @vertex_children_map[cell].do |next_cell|
    traverse_from(next_cell)
  end
  @visited.add(cell)
end
```

  - e.g. [Friend Circles](https://leetcode.com/problems/friend-circles/) <br>
  - e.g. [Shortest Bridge](https://leetcode.com/problems/shortest-bridge/) <br>
  - e.g. [Number of Islands](https://leetcode.com/problems/number-of-islands/) <br>
  - e.g. [Max area of Island](https://leetcode.com/problems/max-area-of-island/) <br>
  - e.g. [Account Merge](https://leetcode.com/problems/accounts-merge/) <br>

*有向图查找connected components要复杂的多，这里不做探讨*


### 有向图 Topological Sort 问题： Graph => 任意路径 (array)

给定一系列先后关系 (parent -> children) ，求一条尊重所有这些先后关系的路径
从所有点出发DFS，用@visiting防止circle 用ordered hash @visited记录所有访问过的点。最后将@visited反向。

**topological sort关注的是整个graph的访问而不是每一个section，也就是`@visited`**


  - e.g. [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/)
  - e.g. [Course Schedule]
  - e.g. [Course Schedule II]
  - e.g. [Dependency Resolver]

### 单点出发求满足条件的单条路径问题： 见 # backtracking

`@visiting`改成hash，找到满足条件的路径时raise error退出，或放入output array

- 如果edge附带其他信息或者并不与 `[parent, children]` pair 一一对应，那么`visited`应该记录ticket_ids 而不是nodes
  - e.g. [Reconstruct Itinerary]

## Tree

- 需要按层访问 => BFS

- 访问/查找节点，与tree的结构无关 => DFS (preorder, inorder, postorder)

- 与tree的结构有关的问题 => Divide and Conquer
  - 首先identify 需要从subtree获得哪些信息才能够得到题意要求的结论 (e.g. 是不是BST)
  - 有些情况下还需要看给subtree什么信息
  - 那么当前tree也需要返回这些信息，如何把left tree和right tree的这些信息组合起来
  - globally，我们需要更新哪些信息？(e.g. 我们每次递归只关注以当前node为root的tree的结论，需要更新全局结论, 这种情形尤其注意不能early return因为会错过right tree）


## BST 问题

BST问题总是可以先思考，如果是sorted array，这个问题如何解决？然后有两种解决办法
- 如果对sorted array我们会binary search，那么根据root的大小来决定对left tree或者right tree 进行 traverse, 根据问题需要的输出顺序决定inorder或者preorder traversal  (比如range sum 就可以任意选择)
```Ruby
def search_recursive(node)
  return if node.nil?

  traverse(node.left) if @low_bound < node.val
  visit(node)
  traverse(node.right) if node.val < @high_bound
end

def search_iterative(node, target)
  while node
    return node if node.val == target
    if target < node.val
      node = node.left
    else
      node = node.right
    end
  end
end
```
  - e.g. [Range Sum BST](https://leetcode.com/problems/range-sum-of-bst/)
  - e.g. [Inorder Successor in BST](https://leetcode.com/problems/inorder-successor-in-bst/)
  - e.g. [Closest Binary Search Tree Value](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)


- 如果对sorted array我们会linear search，那么进行inorder traversal. `visit(node)` 访问当前node的部分，可以想象成在array的循环内会写的内容

  - e.g. [kth smallest element in BST]()
  - e.g. [Validate Binary Search Tree]

## List to Tree 问题 - 线性结构转换成树状结构的问题

总是用divide and conquer的思路，将一个element转换成root，一部分转换成left tree，另一部分转换成right tree.

> 只不过与其在递归的每一层查找分界点，可以在**横向**向右推进cursor，同时在**纵向**往深处递归. 这样的话，每次cursor前进的速度和递归构建root node的速度一样。类似于linkedlist转换成一个array (我们的递归也无非就是一个形式不一样的iterator)，因此总是能保证当前cursor指向的element就是我们当前递归深度需要的element.

1. [Calculator](https://leetcode.com/problems/basic-calculator-iii/)  (计算器的计算本质上是树状结构）
2. [Serialize and Deserialize BST](https://leetcode.com/problems/serialize-and-deserialize-bst/)
3. [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)
4. [Convert Sorted List to a BST](https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree/)

## 缓存 (buffer) 问题

数据的流向： 输出 <= buffer (pool) <= 数据源

1. 从pool里拿数据
2. pool从数据源补充数据
3. 直到 已经拿够数据，或者pool已掏空，whichever come first

这个pool，如果是先进先出，那么用 `queue`， 如果每次需要拿最大或最小，则使用 `Heap` 即 `"Priority Queue"`

> e.g.  https://leetcode.com/problems/read-n-characters-given-read4-ii-call-multiple-times/

## 查找 Kth Element 问题

对于 N sorted sequence, 用min heap `O(klgn)` (或binary search) 见：Array - Intersection / Merge section

> e.g. [Kth Smallest Element in a Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/)
> e.g. [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)

对于 sorted sequence, 用 binary search

> e.g. [Missing Element In Sorted Array](https://leetcode.com/problems/missing-element-in-sorted-array/)

对于 unsorted collection，用max heap of size k (如果是kth largest 就是minheap), Time Complexity: `O(nlgk)`

> e.g. [kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/)

如果value的范围有限, 也可以用bucket来记录value的分布, 进而得到 kth largest or kth smallest

> e.g. [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) *这里频率最大也就是·`O(n)`*

## 抵消问题 (Offset)

用stack来记录需要抵消的元素，这个元素需要包含抵消处理时需要的所有信息。

- e.g. [Asteroid Collision](https://leetcode.com/problems/asteroid-collision/)

当需要每次抵消多个相同元素时，用一个 `Struct.new(:value, :frequency)` 来代替原始的元素

- e.g. [Remove All Adjacent Duplicates in String II](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/)
- e.g. [Exclusive Time of Functions](https://leetcode.com/problems/exclusive-time-of-functions/)

当只有正反两种元素并且我们只在意他们的数量，而不在意他们的位置是，可以用变量来记录他们的数量(balance)

- e.g. [Minimum Remove to Make Valid Parentheses](https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/)

对抵消的元素有先后顺序的情况，比如括号，stack里可以存元素的index，这样在抵消时还可以检查先后顺序。

- e.g. [Longest Valid Parentheses]

*对于一次遍历时无法做出的选择，比如左括号与右括号如何配对, 可以考虑两次遍历*
- e.g. [Valid Parenthesis String](https://leetcode.com/problems/valid-parenthesis-string/)

当offset问题需要优化到 `O(1)` 空间时，因为这类问题后面可以抵消前面的属性，可以考虑从后往前遍历

- e.g. [Backspace String Compare]


## Palindrome问题

1. Expand around center
2. Dynamic Programming

## Binary Search问题

具有递增递减趋势的array 或者 有限定范围的整数range 查找符合条件的元素，首先想到用binary search找中间点，然后问题的关键在于如何选择往左还是往右

1. 我们知道的信息，无非就是头尾的index，中间的index，以及头尾值和中间值
2. 通过这些信息来决定往左还是往右查找

e.g. [Single Element in a Sorted Array](https://leetcode.com/problems/single-element-in-a-sorted-array/) (通过index来判断)

e.g. [Missing Element in Sorted Array](https://leetcode.com/problems/missing-element-in-sorted-array/) (通过index以及值来判断)

## Unique Path
