import pygame
import random

# Pygame setup
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
BAR_WIDTH = 10
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Algorithm Visualization")
clock = pygame.time.Clock()

# Generate random bars
def generate_bars(n, max_height):
    return [random.randint(10, max_height) for _ in range(n)]

# Draw bars on the screen
def draw_bars(bars, color_indices=[], special_color=RED):
    screen.fill(WHITE)
    for i, height in enumerate(bars):
        color = special_color if i in color_indices else BLUE
        pygame.draw.rect(screen, color, [i * BAR_WIDTH, HEIGHT - height, BAR_WIDTH, height])
    pygame.display.update()

# Event handler to keep Pygame responsive
def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

# Bubble Sort
def bubble_sort(bars):
    n = len(bars)
    for i in range(n):
        for j in range(n - i - 1):
            check_events()
            if bars[j] > bars[j + 1]:
                bars[j], bars[j + 1] = bars[j + 1], bars[j]
                draw_bars(bars, color_indices=[j, j + 1])
                clock.tick(30)
    draw_bars(bars, special_color=GREEN)

# Selection Sort
def selection_sort(bars):
    n = len(bars)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            check_events()
            if bars[j] < bars[min_idx]:
                min_idx = j
            draw_bars(bars, color_indices=[j, min_idx], special_color=YELLOW)
            clock.tick(30)
        bars[i], bars[min_idx] = bars[min_idx], bars[i]
        draw_bars(bars, color_indices=[i, min_idx])
    draw_bars(bars, special_color=GREEN)

# Insertion Sort
def insertion_sort(bars):
    for i in range(1, len(bars)):
        key = bars[i]
        j = i - 1
        while j >= 0 and key < bars[j]:
            check_events()
            bars[j + 1] = bars[j]
            j -= 1
            draw_bars(bars, color_indices=[j + 1, i], special_color=YELLOW)
            clock.tick(30)
        bars[j + 1] = key
        draw_bars(bars)
    draw_bars(bars, special_color=GREEN)

# Merge Sort
def merge_sort(bars, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort(bars, left, mid)
        merge_sort(bars, mid + 1, right)
        merge(bars, left, mid, right)

def merge(bars, left, mid, right):
    left_part = bars[left:mid + 1]
    right_part = bars[mid + 1:right + 1]
    
    i = j = 0
    k = left
    while i < len(left_part) and j < len(right_part):
        check_events()
        if left_part[i] <= right_part[j]:
            bars[k] = left_part[i]
            i += 1
        else:
            bars[k] = right_part[j]
            j += 1
        k += 1
        draw_bars(bars, color_indices=[k])
        clock.tick(30)

    while i < len(left_part):
        bars[k] = left_part[i]
        i += 1
        k += 1
        draw_bars(bars, color_indices=[k])
        clock.tick(30)

    while j < len(right_part):
        bars[k] = right_part[j]
        j += 1
        k += 1
        draw_bars(bars, color_indices=[k])
        clock.tick(30)

# Quick Sort
def quick_sort(bars, low, high):
    if low < high:
        pi = partition(bars, low, high)
        quick_sort(bars, low, pi - 1)
        quick_sort(bars, pi + 1, high)

def partition(bars, low, high):
    pivot = bars[high]
    i = low - 1
    for j in range(low, high):
        check_events()
        if bars[j] < pivot:
            i += 1
            bars[i], bars[j] = bars[j], bars[i]
            draw_bars(bars, color_indices=[i, j])
            clock.tick(30)
    bars[i + 1], bars[high] = bars[high], bars[i + 1]
    draw_bars(bars, color_indices=[i + 1, high])
    clock.tick(30)
    return i + 1

# Bogo Sort
def bogo_sort(bars):
    def is_sorted(b):
        return all(b[i] <= b[i + 1] for i in range(len(b) - 1))

    while not is_sorted(bars):
        check_events()
        random.shuffle(bars)
        draw_bars(bars)
        clock.tick(10)
    draw_bars(bars, special_color=GREEN)

# Heap Sort
def heapify(bars, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and bars[left] > bars[largest]:
        largest = left

    if right < n and bars[right] > bars[largest]:
        largest = right

    if largest != i:
        bars[i], bars[largest] = bars[largest], bars[i]
        draw_bars(bars, color_indices=[i, largest])
        clock.tick(30)
        heapify(bars, n, largest)

def heap_sort(bars):
    n = len(bars)
    for i in range(n // 2 - 1, -1, -1):
        check_events()
        heapify(bars, n, i)

    for i in range(n - 1, 0, -1):
        check_events()
        bars[i], bars[0] = bars[0], bars[i]
        draw_bars(bars, color_indices=[0, i])
        clock.tick(30)
        heapify(bars, i, 0)
    draw_bars(bars, special_color=GREEN)

# Counting Sort
def counting_sort(bars):
    max_val = max(bars)
    count = [0] * (max_val + 1)
    output = [0] * len(bars)

    for bar in bars:
        count[bar] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for bar in reversed(bars):
        check_events()
        output[count[bar] - 1] = bar
        count[bar] -= 1
        draw_bars(output, color_indices=[count[bar]])
        clock.tick(30)

    for i in range(len(bars)):
        bars[i] = output[i]
    draw_bars(bars, special_color=GREEN)

# Radix Sort
def counting_sort_radix(bars, exp):
    n = len(bars)
    output = [0] * n
    count = [0] * 10

    for bar in bars:
        index = (bar // exp) % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in reversed(range(n)):
        check_events()
        index = (bars[i] // exp) % 10
        output[count[index] - 1] = bars[i]
        count[index] -= 1
        draw_bars(output, color_indices=[count[index]])
        clock.tick(30)

    for i in range(n):
        bars[i] = output[i]

def radix_sort(bars):
    max_val = max(bars)
    exp = 1
    while max_val // exp > 0:
        check_events()
        counting_sort_radix(bars, exp)
        exp *= 10
    draw_bars(bars, special_color=GREEN)

# Bucket Sort
def bucket_sort(bars):
    max_val = max(bars)
    size = max_val // len(bars) + 1
    buckets = [[] for _ in range(size)]

    for bar in bars:
        check_events()
        buckets[bar // size].append(bar)
        draw_bars(bars)
        clock.tick(30)

    index = 0
    for bucket in buckets:
        for bar in sorted(bucket):
            check_events()
            bars[index] = bar
            index += 1
            draw_bars(bars, color_indices=[index])
            clock.tick(30)
    draw_bars(bars, special_color=GREEN)

# Main program loop
def main():
    algorithms = {
        "bubble": bubble_sort,
        "selection": selection_sort,
        "insertion": insertion_sort,
        "merge": lambda bars: merge_sort(bars, 0, len(bars) - 1),
        "quick": lambda bars: quick_sort(bars, 0, len(bars) - 1),
        "bogo": bogo_sort,
        "heap": heap_sort,
        "counting": counting_sort,
        "radix": radix_sort,
        "bucket": bucket_sort,
    }

    print("Desired sorting algorithm (bubble, selection, insertion, merge, quick, bogo, heap, counting, radix, bucket):")
    algorithm_name = input().strip().lower()

    if algorithm_name not in algorithms:
        print("Invalid algorithm")
        return

    num_bars = WIDTH // BAR_WIDTH
    max_height = HEIGHT - 50
    bars = generate_bars(num_bars, max_height)
    draw_bars(bars)

    algorithms[algorithm_name](bars)

    print("Sorting complete! Press close button to exit.")
    while True:
        check_events()
        clock.tick(FPS)

if __name__ == "__main__":
    main()