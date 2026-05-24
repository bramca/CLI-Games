import curses
import random
import sys
import os
import time

username = "no name"
n_snippets = 10

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
    R"""struct Node {
    int data;
    struct Node* next;
};

struct Node* insertFront(struct Node* head, int val) {
    struct Node* newNode = malloc(sizeof(struct Node));
    newNode->data = val;
    newNode->next = head;
    return newNode;
}""",
    R"""struct Node* reverseList(struct Node* head) {
    struct Node* prev = NULL;
    struct Node* curr = head;
    struct Node* next;
    while (curr != NULL) {
        next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}""",
    R"""void inorder(struct Node* root) {
    if (root == NULL) return;
    inorder(root->left);
    printf("%d ", root->data);
    inorder(root->right);
}""",
    R"""struct Node* searchBST(struct Node* root, int key) {
    while (root != NULL && root->data != key) {
        if (key < root->data)
            root = root->left;
        else
            root = root->right;
    }
    return root;
}""",
    R"""void enqueue(int q[], int* rear, int size, int val) {
    if (*rear == size - 1) return;
    q[++(*rear)] = val;
}

int dequeue(int q[], int* front, int* rear) {
    if (*front > *rear) return -1;
    return q[(*front)++];
}""",
    R"""#define MAX 100

typedef struct {
    int data[MAX];
    int top;
} Stack;

void push(Stack* s, int val) {
    if (s->top < MAX - 1)
        s->data[++s->top] = val;
}

int pop(Stack* s) {
    if (s->top == -1) return -1;
    return s->data[s->top--];
}""",
    R"""struct TreeNode {
    int val;
    struct TreeNode* left;
    struct TreeNode* right;
};

struct TreeNode* createNode(int val) {
    struct TreeNode* n = malloc(sizeof(struct TreeNode));
    n->val = val;
    n->left = n->right = NULL;
    return n;
}""",
    R"""void caesarCipher(char* text, int shift) {
    for (int i = 0; text[i] != '\0'; i++) {
        if (text[i] >= 'a' && text[i] <= 'z')
            text[i] = (text[i] - 'a' + shift) % 26 + 'a';
        else if (text[i] >= 'A' && text[i] <= 'Z')
            text[i] = (text[i] - 'A' + shift) % 26 + 'A';
    }
}""",
    R"""void xorCipher(char* data, int len, char key) {
    for (int i = 0; i < len; i++)
        data[i] ^= key;
}""",
    R"""unsigned long djb2(const char* str) {
    unsigned long hash = 5381;
    int c;
    while ((c = *str++))
        hash = ((hash << 5) + hash) + c;
    return hash;
}""",
    R"""char* vigenereEncrypt(const char* text, const char* key) {
    int len = strlen(text);
    char* result = malloc(len + 1);
    for (int i = 0; i < len; i++) {
        char t = text[i] - 'A';
        char k = key[i % strlen(key)] - 'A';
        result[i] = (t + k) % 26 + 'A';
    }
    result[len] = '\0';
    return result;
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


def main(stdscr):
    curses.curs_set(2)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_WHITE, -1)

    stdscr.nodelay(0)
    stdscr.clear()

    snippets = random.sample(C_SNIPPETS, n_snippets)

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
    curses.wrapper(main)
