import curses
import random
import sys
import os
import time

username = "no name"
n_snippets = 5

C_SNIPPETS = [
    R"""int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}""",
    R"""int gcd(int a, int b) {
    while (b != 0) {
        int t = b;
        b = a % b;
        a = t;
    }
    return a;
}""",
    R"""void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int tmp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = tmp;
            }
        }
    }
}""",
    R"""int fibonacci(int n) {
    if (n <= 1) return n;
    int a = 0, b = 1, c;
    for (int i = 2; i <= n; i++) {
        c = a + b;
        a = b;
        b = c;
    }
    return b;
}""",
    R"""bool isPrime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (int i = 5; i * i <= n; i += 6)
        if (n % i == 0 || n % (i + 2) == 0)
            return false;
    return true;
}""",
    R"""int binarySearch(int arr[], int l, int r, int x) {
    while (l <= r) {
        int m = l + (r - l) / 2;
        if (arr[m] == x) return m;
        if (arr[m] < x) l = m + 1;
        else r = m - 1;
    }
    return -1;
}""",
    R"""void selectionSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++)
            if (arr[j] < arr[minIdx])
                minIdx = j;
        int tmp = arr[i];
        arr[i] = arr[minIdx];
        arr[minIdx] = tmp;
    }
}""",
    R"""int linearSearch(int arr[], int n, int x) {
    for (int i = 0; i < n; i++)
        if (arr[i] == x)
            return i;
    return -1;
}""",
    R"""int sumArray(int arr[], int n) {
    int sum = 0;
    for (int i = 0; i < n; i++)
        sum += arr[i];
    return sum;
}""",
    R"""int strLen(const char* s) {
    int len = 0;
    while (s[len] != '\0') len++;
    return len;
}""",
    R"""void reverseArray(int arr[], int n) {
    for (int i = 0; i < n / 2; i++) {
        int tmp = arr[i];
        arr[i] = arr[n - 1 - i];
        arr[n - 1 - i] = tmp;
    }
}""",
    R"""void insertionSort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}""",
    R"""int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++)
        if (arr[j] <= pivot) {
            i++;
            int tmp = arr[i];
            arr[i] = arr[j];
            arr[j] = tmp;
        }
    int tmp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = tmp;
    return i + 1;
}""",
    R"""bool isPalindrome(const char* s) {
    int left = 0;
    int right = strlen(s) - 1;
    while (left < right) {
        if (s[left] != s[right])
            return false;
        left++;
        right--;
    }
    return true;
}""",
    R"""int power(int base, int exp) {
    if (exp == 0) return 1;
    if (exp % 2 == 0) {
        int half = power(base, exp / 2);
        return half * half;
    }
    return base * power(base, exp - 1);
}""",
    R"""int countChar(const char* s, char c) {
    int count = 0;
    for (int i = 0; s[i] != '\0'; i++)
        if (s[i] == c)
            count++;
    return count;
}""",
    R"""int findMax(int arr[], int n) {
    int max = arr[0];
    for (int i = 1; i < n; i++)
        if (arr[i] > max)
            max = arr[i];
    return max;
}""",
    R"""void towerOfHanoi(int n, char from, char to, char aux) {
    if (n == 1) {
        printf("Move 1 from %c to %c\n", from, to);
        return;
    }
    towerOfHanoi(n - 1, from, aux, to);
    printf("Move %d from %c to %c\n", n, from, to);
    towerOfHanoi(n - 1, aux, to, from);
}""",
    R"""int digitSum(int n) {
    int sum = 0;
    while (n != 0) {
        sum += n % 10;
        n /= 10;
    }
    return sum;
}""",
    R"""bool isArmstrong(int n) {
    int sum = 0, tmp = n, digits = 0;
    while (tmp != 0) {
        tmp /= 10;
        digits++;
    }
    tmp = n;
    while (tmp != 0) {
        int d = tmp % 10;
        int p = 1;
        for (int i = 0; i < digits; i++)
            p *= d;
        sum += p;
        tmp /= 10;
    }
    return sum == n;
}""",
]

RUST_SNIPPETS = [
    R"""fn factorial(n: u32) -> u32 {
    if n <= 1 {
        return 1;
    }
    n * factorial(n - 1)
}""",
    R"""fn gcd(a: u32, b: u32) -> u32 {
    let mut a = a;
    let mut b = b;
    while b != 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    a
}""",
    R"""fn bubble_sort(arr: &mut [i32]) {
    let n = arr.len();
    for i in 0..n {
        for j in 0..n - i - 1 {
            if arr[j] > arr[j + 1] {
                arr.swap(j, j + 1);
            }
        }
    }
}""",
    R"""fn fibonacci(n: u32) -> u32 {
    if n <= 1 {
        return n;
    }
    let (mut a, mut b) = (0, 1);
    for _ in 2..=n {
        let c = a + b;
        a = b;
        b = c;
    }
    b
}""",
    R"""fn is_prime(n: u32) -> bool {
    if n <= 1 {
        return false;
    }
    if n <= 3 {
        return true;
    }
    if n % 2 == 0 || n % 3 == 0 {
        return false;
    }
    let mut i = 5;
    while i * i <= n {
        if n % i == 0 || n % (i + 2) == 0 {
            return false;
        }
        i += 6;
    }
    true
}""",
    R"""fn binary_search(arr: &[i32], x: i32) -> i32 {
    let (mut l, mut r) = (0, arr.len() as i32 - 1);
    while l <= r {
        let m = l + (r - l) / 2;
        if arr[m as usize] == x {
            return m;
        }
        if arr[m as usize] < x {
            l = m + 1;
        } else {
            r = m - 1;
        }
    }
    -1
}""",
    R"""fn selection_sort(arr: &mut [i32]) {
    let n = arr.len();
    for i in 0..n - 1 {
        let mut min_idx = i;
        for j in i + 1..n {
            if arr[j] < arr[min_idx] {
                min_idx = j;
            }
        }
        arr.swap(i, min_idx);
    }
}""",
    R"""fn linear_search(arr: &[i32], x: i32) -> i32 {
    for (i, &val) in arr.iter().enumerate() {
        if val == x {
            return i as i32;
        }
    }
    -1
}""",
    R"""fn sum_array(arr: &[i32]) -> i32 {
    let mut sum = 0;
    for &x in arr {
        sum += x;
    }
    sum
}""",
    R"""fn str_len(s: &str) -> usize {
    let mut len = 0;
    for _ in s.chars() {
        len += 1;
    }
    len
}""",
    R"""fn reverse_array(arr: &mut [i32]) {
    let n = arr.len();
    for i in 0..n / 2 {
        arr.swap(i, n - 1 - i);
    }
}""",
    R"""fn insertion_sort(arr: &mut [i32]) {
    for i in 1..arr.len() {
        let key = arr[i];
        let mut j = i as i32 - 1;
        while j >= 0 && arr[j as usize] > key {
            arr[(j + 1) as usize] = arr[j as usize];
            j -= 1;
        }
        arr[(j + 1) as usize] = key;
    }
}""",
    R"""fn partition(arr: &mut [i32]) -> usize {
    let pivot = arr[arr.len() - 1];
    let mut i = 0;
    for j in 0..arr.len() - 1 {
        if arr[j] <= pivot {
            arr.swap(i, j);
            i += 1;
        }
    }
    arr.swap(i, arr.len() - 1);
    i
}""",
    R"""fn is_palindrome(s: &str) -> bool {
    let chars: Vec<char> = s.chars().collect();
    let (mut left, mut right) = (0, chars.len() - 1);
    while left < right {
        if chars[left] != chars[right] {
            return false;
        }
        left += 1;
        right -= 1;
    }
    true
}""",
    R"""fn power(base: u32, exp: u32) -> u32 {
    if exp == 0 {
        return 1;
    }
    if exp % 2 == 0 {
        let half = power(base, exp / 2);
        half * half
    } else {
        base * power(base, exp - 1)
    }
}""",
    R"""fn count_char(s: &str, c: char) -> usize {
    let mut count = 0;
    for ch in s.chars() {
        if ch == c {
            count += 1;
        }
    }
    count
}""",
    R"""fn find_max(arr: &[i32]) -> i32 {
    let mut max = arr[0];
    for &x in &arr[1..] {
        if x > max {
            max = x;
        }
    }
    max
}""",
    R"""fn tower_of_hanoi(n: u32, from: char, to: char, aux: char) {
    if n == 1 {
        println!("Move 1 from {from} to {to}");
        return;
    }
    tower_of_hanoi(n - 1, from, aux, to);
    println!("Move {n} from {from} to {to}");
    tower_of_hanoi(n - 1, aux, to, from);
}""",
    R"""fn digit_sum(mut n: u32) -> u32 {
    let mut sum = 0;
    while n != 0 {
        sum += n % 10;
        n /= 10;
    }
    sum
}""",
    R"""fn is_armstrong(n: u32) -> bool {
    let mut sum = 0;
    let mut tmp = n;
    let mut digits = 0;
    while tmp != 0 {
        tmp /= 10;
        digits += 1;
    }
    tmp = n;
    while tmp != 0 {
        let d = tmp % 10;
        let mut p = 1;
        for _ in 0..digits {
            p *= d;
        }
        sum += p;
        tmp /= 10;
    }
    sum == n
}""",
    R"""struct Node {
    data: i32,
    next: Option<Box<Node>>,
}

fn insert_front(head: Option<Box<Node>>, val: i32) -> Option<Box<Node>> {
    Some(Box::new(Node {
        data: val,
        next: head,
    }))
}""",
    R"""fn reverse_list(head: Option<Box<Node>>) -> Option<Box<Node>> {
    let mut prev = None;
    let mut curr = head;
    while let Some(mut node) = curr {
        curr = node.next.take();
        node.next = prev;
        prev = Some(node);
    }
    prev
}""",
    R"""fn inorder(root: Option<&Box<TreeNode>>) {
    if let Some(node) = root {
        inorder(node.left.as_ref());
        println!("{} ", node.val);
        inorder(node.right.as_ref());
    }
}""",
    R"""fn search_bst(root: Option<&Box<TreeNode>>, key: i32) -> Option<&Box<TreeNode>> {
    let mut curr = root;
    while let Some(node) = curr {
        if node.val == key {
            return curr;
        }
        if key < node.val {
            curr = node.left.as_ref();
        } else {
            curr = node.right.as_ref();
        }
    }
    None
}""",
    R"""fn enqueue(q: &mut Vec<i32>, val: i32) {
    q.push(val);
}

fn dequeue(q: &mut Vec<i32>) -> Option<i32> {
    if q.is_empty() {
        return None;
    }
    Some(q.remove(0))
}""",
    R"""struct Stack {
    data: Vec<i32>,
}

impl Stack {
    fn push(&mut self, val: i32) {
        self.data.push(val);
    }

    fn pop(&mut self) -> Option<i32> {
        self.data.pop()
    }
}""",
    R"""struct TreeNode {
    val: i32,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

fn create_node(val: i32) -> Option<Box<TreeNode>> {
    Some(Box::new(TreeNode {
        val,
        left: None,
        right: None,
    }))
}""",
    R"""fn caesar_cipher(text: &mut [u8], shift: u8) {
    for c in text.iter_mut() {
        if *c >= b'a' && *c <= b'z' {
            *c = (*c - b'a' + shift) % 26 + b'a';
        } else if *c >= b'A' && *c <= b'Z' {
            *c = (*c - b'A' + shift) % 26 + b'A';
        }
    }
}""",
    R"""fn xor_cipher(data: &mut [u8], key: u8) {
    for byte in data.iter_mut() {
        *byte ^= key;
    }
}""",
    R"""fn djb2(str: &[u8]) -> u64 {
    let mut hash: u64 = 5381;
    for &c in str {
        hash = ((hash << 5).wrapping_add(hash)).wrapping_add(c as u64);
    }
    hash
}""",
    R"""fn vigenere_encrypt(text: &str, key: &str) -> String {
    let key_bytes = key.as_bytes();
    let mut result = String::new();
    for (i, c) in text.bytes().enumerate() {
        let t = c - b'A';
        let k = key_bytes[i % key.len()] - b'A';
        result.push(((t + k) % 26 + b'A') as char);
    }
    result
}""",
]

ZIG_SNIPPETS = [
    R"""fn factorial(n: u32) u32 {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}""",
    R"""fn gcd(a: u32, b: u32) u32 {
    var x = a;
    var y = b;
    while (y != 0) {
        const t = y;
        y = x % y;
        x = t;
    }
    return x;
}""",
    R"""fn bubbleSort(arr: []i32) void {
    const n = arr.len;
    for (0..n) |i| {
        for (0..n - i - 1) |j| {
            if (arr[j] > arr[j + 1]) {
                const tmp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = tmp;
            }
        }
    }
}""",
    R"""fn fibonacci(n: u32) u32 {
    if (n <= 1) return n;
    var a: u32 = 0;
    var b: u32 = 1;
    for (2..n + 1) |_| {
        const c = a + b;
        a = b;
        b = c;
    }
    return b;
}""",
    R"""fn isPrime(n: u32) bool {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 or n % 3 == 0) return false;
    var i: u32 = 5;
    while (i * i <= n) {
        if (n % i == 0 or n % (i + 2) == 0) return false;
        i += 6;
    }
    return true;
}""",
    R"""fn binarySearch(arr: []const i32, x: i32) i32 {
    var l: usize = 0;
    var r: usize = arr.len;
    while (l < r) {
        const m = l + (r - l) / 2;
        if (arr[m] == x) return @intCast(m);
        if (arr[m] < x) {
            l = m + 1;
        } else {
            r = m;
        }
    }
    return -1;
}""",
    R"""fn selectionSort(arr: []i32) void {
    const n = arr.len;
    for (0..n - 1) |i| {
        var minIdx = i;
        for (i + 1..n) |j| {
            if (arr[j] < arr[minIdx]) {
                minIdx = j;
            }
        }
        const tmp = arr[i];
        arr[i] = arr[minIdx];
        arr[minIdx] = tmp;
    }
}""",
    R"""fn linearSearch(arr: []const i32, x: i32) i32 {
    for (arr, 0..) |val, i| {
        if (val == x) return @intCast(i);
    }
    return -1;
}""",
    R"""fn sumArray(arr: []const i32) i32 {
    var sum: i32 = 0;
    for (arr) |x| {
        sum += x;
    }
    return sum;
}""",
    R"""fn strLen(s: []const u8) usize {
    var len: usize = 0;
    for (s) |_| {
        len += 1;
    }
    return len;
}""",
    R"""fn reverseArray(arr: []i32) void {
    const n = arr.len;
    for (0..n / 2) |i| {
        const tmp = arr[i];
        arr[i] = arr[n - 1 - i];
        arr[n - 1 - i] = tmp;
    }
}""",
    R"""fn insertionSort(arr: []i32) void {
    var i: usize = 1;
    while (i < arr.len) {
        const key = arr[i];
        var j: i32 = @intCast(i - 1);
        while (j >= 0 and arr[@intCast(j)] > key) {
            arr[@intCast(j + 1)] = arr[@intCast(j)];
            j -= 1;
        }
        arr[@intCast(j + 1)] = key;
        i += 1;
    }
}""",
    R"""fn partition(arr: []i32) usize {
    const pivot = arr[arr.len - 1];
    var i: usize = 0;
    for (0..arr.len - 1) |j| {
        if (arr[j] <= pivot) {
            const tmp = arr[i];
            arr[i] = arr[j];
            arr[j] = tmp;
            i += 1;
        }
    }
    const tmp = arr[i];
    arr[i] = arr[arr.len - 1];
    arr[arr.len - 1] = tmp;
    return i;
}""",
    R"""fn isPalindrome(s: []const u8) bool {
    var left: usize = 0;
    var right: usize = s.len - 1;
    while (left < right) {
        if (s[left] != s[right]) return false;
        left += 1;
        right -= 1;
    }
    return true;
}""",
    R"""fn power(base: u32, exp: u32) u32 {
    if (exp == 0) return 1;
    if (exp % 2 == 0) {
        const half = power(base, exp / 2);
        return half * half;
    }
    return base * power(base, exp - 1);
}""",
    R"""fn countChar(s: []const u8, c: u8) usize {
    var count: usize = 0;
    for (s) |ch| {
        if (ch == c) count += 1;
    }
    return count;
}""",
    R"""fn findMax(arr: []const i32) i32 {
    var max = arr[0];
    for (arr[1..]) |x| {
        if (x > max) max = x;
    }
    return max;
}""",
    R"""fn towerOfHanoi(n: u32, from: u8, to: u8, aux: u8) void {
    if (n == 1) {
        std.debug.print("Move 1 from {c} to {c}\n", .{ from, to });
        return;
    }
    towerOfHanoi(n - 1, from, aux, to);
    std.debug.print("Move {} from {c} to {c}\n", .{ n, from, to });
    towerOfHanoi(n - 1, aux, to, from);
}""",
    R"""fn digitSum(n: u32) u32 {
    var sum: u32 = 0;
    var tmp = n;
    while (tmp != 0) {
        sum += tmp % 10;
        tmp /= 10;
    }
    return sum;
}""",
    R"""fn isArmstrong(n: u32) bool {
    var sum: u32 = 0;
    var tmp = n;
    var digits: u32 = 0;
    while (tmp != 0) {
        tmp /= 10;
        digits += 1;
    }
    tmp = n;
    while (tmp != 0) {
        const d = tmp % 10;
        var p: u32 = 1;
        for (0..digits) |_| {
            p *= d;
        }
        sum += p;
        tmp /= 10;
    }
    return sum == n;
}""",
    R"""const Node = struct {
    data: i32,
    next: ?*Node,
};

fn insertFront(head: ?*Node, allocator: *std.mem.Allocator, val: i32) ?*Node {
    const newNode = allocator.create(Node) catch unreachable;
    newNode.* = .{ .data = val, .next = head };
    return newNode;
}""",
    R"""fn reverseList(head: ?*Node) ?*Node {
    var prev: ?*Node = null;
    var curr = head;
    while (curr) |node| {
        const next = node.next;
        node.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}""",
    R"""fn inorder(root: ?*TreeNode) void {
    if (root) |node| {
        inorder(node.left);
        std.debug.print("{} ", .{node.val});
        inorder(node.right);
    }
}""",
    R"""fn searchBST(root: ?*TreeNode, key: i32) ?*TreeNode {
    var curr = root;
    while (curr) |node| {
        if (node.val == key) return curr;
        if (key < node.val) {
            curr = node.left;
        } else {
            curr = node.right;
        }
    }
    return null;
}""",
    R"""fn enqueue(q: []i32, rear: *usize, size: usize, val: i32) void {
    if (rear.* == size - 1) return;
    rear.* += 1;
    q[rear.*] = val;
}

fn dequeue(q: []i32, front: *usize, rear: *usize) ?i32 {
    if (front.* > rear.*) return null;
    const val = q[front.*];
    front.* += 1;
    return val;
}""",
    R"""const Stack = struct {
    data: [100]i32 = undefined,
    top: i32 = -1,

    fn push(self: *Stack, val: i32) void {
        if (self.top < 99) {
            self.top += 1;
            self.data[@intCast(self.top)] = val;
        }
    }

    fn pop(self: *Stack) ?i32 {
        if (self.top == -1) return null;
        const val = self.data[@intCast(self.top)];
        self.top -= 1;
        return val;
    }
};""",
    R"""const TreeNode = struct {
    val: i32,
    left: ?*TreeNode,
    right: ?*TreeNode,
};

fn createNode(allocator: *std.mem.Allocator, val: i32) ?*TreeNode {
    const node = allocator.create(TreeNode) catch return null;
    node.* = .{ .val = val, .left = null, .right = null };
    return node;
}""",
    R"""fn caesarCipher(text: []u8, shift: u8) void {
    for (text) |*c| {
        if (c.* >= 'a' and c.* <= 'z') {
            c.* = (c.* - 'a' + shift) % 26 + 'a';
        } else if (c.* >= 'A' and c.* <= 'Z') {
            c.* = (c.* - 'A' + shift) % 26 + 'A';
        }
    }
}""",
    R"""fn xorCipher(data: []u8, key: u8) void {
    for (data) |*byte| {
        byte.* ^= key;
    }
}""",
    R"""fn djb2(str: []const u8) u64 {
    var hash: u64 = 5381;
    for (str) |c| {
        hash = ((hash << 5) +% hash) +% c;
    }
    return hash;
}""",
    R"""fn vigenereEncrypt(text: []const u8, key: []const u8, result: []u8) void {
    for (text, 0..) |c, i| {
        const t = c - 'A';
        const k = key[i % key.len] - 'A';
        result[i] = (t + k) % 26 + 'A';
    }
}""",
]


def write_highscores(highscore_file, score, username):
    if score > 0:
        highscores = []
        if os.path.exists(highscore_file):
            file = open(highscore_file, "r")
            highscores = file.read().splitlines()
            file.close()
        file = open(highscore_file, "w")
        highscores.append("{} - {}".format(score, username))
        highscores.sort(key=lambda x: int(x.split("-")[0]), reverse=True)
        file.write("\n".join(highscores))
        file.close()


def draw_progress(stdscr, y, x, correct, incorrect, elapsed):
    total = correct + incorrect
    wpm = (total / 5) / (elapsed / 60) if elapsed > 0 and total > 0 else 0
    stdscr.addstr(y, x,
        "Correct: {}  Incorrect: {}  Total: {}  WPM: {:.1f}".format(
            correct, incorrect, total, wpm))
    if total > 0:
        pct = correct * 100 // total
        bar_width = 40
        filled = bar_width * correct // total
        bar = "[" + "#" * filled + "." * (bar_width - filled) + "]"
        stdscr.addstr(y + 1, x, "Accuracy: {}%  {}".format(pct, bar))


def run_snippet(stdscr, snippet, start_y, start_x, total_correct, total_incorrect):
    lines = snippet.split("\n")

    flat_positions = []
    for li, line in enumerate(lines):
        for ci in range(len(line)):
            flat_positions.append((li, ci))
        flat_positions.append((li, -1))

    max_y, max_x = stdscr.getmaxyx()

    color_map = {}

    def draw_all():
        for li, line in enumerate(lines):
            for ci, ch in enumerate(line):
                color = color_map.get((li, ci), curses.color_pair(3))
                dy = start_y + 3 + li
                dx = start_x + 2 + ci
                if dy < max_y and dx < max_x:
                    try:
                        stdscr.addstr(dy, dx, ch, color)
                    except curses.error:
                        pass

    draw_all()
    stdscr.refresh()

    pos = 0
    while pos < len(flat_positions):
        li, ci = flat_positions[pos]

        at_eol = ci == -1

        if at_eol:
            dy = start_y + 3 + li
            dx = start_x + 2 + len(lines[li])
        else:
            dy = start_y + 3 + li
            dx = start_x + 2 + ci

        if dy >= max_y or dx >= max_x:
            return None

        if not at_eol:
            stdscr.addstr(dy, dx, lines[li][ci], curses.color_pair(3))
        stdscr.move(dy, dx)

        key = stdscr.getch()

        if key == 27:
            return None

        if key in (127, curses.KEY_BACKSPACE, 8, curses.KEY_DC):
            if pos > 0:
                pos -= 1
                pli, pci = flat_positions[pos]
                if pci != -1:
                    color_map.pop((pli, pci), None)
                    pdy = start_y + 3 + pli
                    pdx = start_x + 2 + pci
                    if pdy < max_y and pdx < max_x:
                        try:
                            stdscr.addstr(pdy, pdx, lines[pli][pci], curses.color_pair(3))
                        except curses.error:
                            pass
                stdscr.refresh()
            continue

        if key in (10, 13, curses.KEY_ENTER):
            if at_eol:
                while pos < len(flat_positions) and flat_positions[pos][0] == li:
                    pos += 1
                if pos < len(flat_positions):
                    next_li = flat_positions[pos][0]
                    while pos < len(flat_positions) and flat_positions[pos][0] == next_li:
                        li, ci = flat_positions[pos]
                        if ci == -1:
                            break
                        ch = lines[li][ci]
                        if ch not in (' ', '\t'):
                            break
                        color_map[(li, ci)] = curses.color_pair(1)
                        total_correct += 1
                        pos += 1
                draw_all()
                stdscr.refresh()
                continue
            else:
                total_incorrect += 1
                continue

        if at_eol:
            total_incorrect += 1
            continue

        typed_char = chr(key) if key < 256 else None
        if typed_char is None:
            continue

        if typed_char == lines[li][ci]:
            color = curses.color_pair(1)
            total_correct += 1
        else:
            color = curses.color_pair(2)
            total_incorrect += 1

        color_map[(li, ci)] = color
        if dy < max_y and dx < max_x:
            try:
                stdscr.addstr(dy, dx, lines[li][ci], color)
            except curses.error:
                pass

        stdscr.refresh()
        pos += 1

    return (total_correct, total_incorrect)


def main(stdscr, snippet_pool):
    curses.curs_set(2)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_WHITE, -1)

    stdscr.nodelay(0)
    stdscr.clear()

    snippets = random.sample(snippet_pool, n_snippets)

    total_correct = 0
    total_incorrect = 0
    snippet_idx = 0
    start_time = time.time()

    while snippet_idx < len(snippets):
        snippet = snippets[snippet_idx]
        lines = snippet.split("\n")
        max_line_len = max(len(l) for l in lines)
        height = len(lines) + 5
        width = max(max_line_len + 4, 60)

        max_y, max_x = stdscr.getmaxyx()
        start_y = max(0, (max_y - height) // 2)
        start_x = max(0, (max_x - width) // 2)

        stdscr.clear()
        header_y = start_y
        header_x = start_x + 2
        draw_progress(stdscr, header_y, header_x, total_correct, total_incorrect,
                      time.time() - start_time)
        if header_y + 2 < max_y:
            stdscr.addstr(header_y + 2, header_x,
                          "Snippet {} of {}  |  ESC to quit".format(
                              snippet_idx + 1, len(snippets)))
        stdscr.refresh()

        result = run_snippet(stdscr, snippet, start_y, start_x,
                             total_correct, total_incorrect)
        if result is None:
            break
        total_correct, total_incorrect = result

        h = start_y + 3 + len(lines) + 1
        if h < max_y:
            stdscr.addstr(h, start_x + 2,
                          "Snippet done! Press any key for next...")
            stdscr.refresh()
            stdscr.getch()

        snippet_idx += 1

    stdscr.clear()
    total = total_correct + total_incorrect
    elapsed = time.time() - start_time
    wpm = (total / 5) / (elapsed / 60) if elapsed > 0 and total > 0 else 0
    accuracy = total_correct * 100 // total if total > 0 else 0
    msg = "All done! Accuracy: {}%  WPM: {:.1f}  ({}/{}) correct".format(
        accuracy, wpm, total_correct, total)
    max_y, max_x = stdscr.getmaxyx()
    stdscr.addstr(max_y // 2, (max_x - len(msg)) // 2, msg)
    stdscr.addstr(max_y // 2 + 2, (max_x - 24) // 2, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()

    write_highscores("typing_highscores.txt", total_correct, username)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = input("Please provide your player name: ")

    if len(sys.argv) > 2:
        lang = sys.argv[2].lower()
    else:
        print("Select language:")
        print("1. C++")
        print("2. Rust")
        print("3. Zig")
        choice = input("Enter number: ")
        lang = { "1": "c++", "2": "rust", "3": "zig" }.get(choice, "c++")

    if "zig" in lang:
        snippet_pool = ZIG_SNIPPETS
    elif "rust" in lang:
        snippet_pool = RUST_SNIPPETS
    else:
        snippet_pool = C_SNIPPETS

    def run(stdscr):
        main(stdscr, snippet_pool)

    curses.wrapper(run)
