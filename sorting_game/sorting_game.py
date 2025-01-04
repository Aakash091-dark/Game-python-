import pygame
import random
import time

# Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ARRAY_SIZE = 50
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class SortingGame:
    def __init__(self):
        self.array = [random.randint(1, SCREEN_HEIGHT) for _ in range(ARRAY_SIZE)]
        self.sorting = False
        self.algorithm = "BubbleSort"
        self.sorted = False

    def draw(self, screen):
        screen.fill(BLACK)
        self.display_algorithm(screen)
        self.draw_array(screen)
        pygame.display.flip()

    def display_algorithm(self, screen):
        font = pygame.font.SysFont('Arial', 24)
        text = font.render(f"Algorithm: {self.algorithm}", True, WHITE)
        screen.blit(text, (10, 10))

    def draw_array(self, screen):
        width = SCREEN_WIDTH // len(self.array)
        for i, value in enumerate(self.array):
            color = GREEN if self.sorted else WHITE
            pygame.draw.rect(screen, color, pygame.Rect(i * width, SCREEN_HEIGHT - value, width, value))

    def sort(self):
        if self.algorithm == "BubbleSort":
            self.bubble_sort()
        elif self.algorithm == "MergeSort":
            self.merge_sort()
        elif self.algorithm == "QuickSort":
            self.quick_sort()

    def bubble_sort(self):
        n = len(self.array)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                self.sorted = True
                time.sleep(0.01)

    def merge_sort(self):
        self.array = self.merge_sort_helper(self.array)

    def merge_sort_helper(self, arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        left = self.merge_sort_helper(left)
        right = self.merge_sort_helper(right)

        return self.merge(left, right)

    def merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def quick_sort(self):
        self.quick_sort_helper(0, len(self.array) - 1)

    def quick_sort_helper(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort_helper(low, pi - 1)
            self.quick_sort_helper(pi + 1, high)

    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        for j in range(low, high):
            if self.array[j] <= pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        return i + 1

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sorting Game")

    game = SortingGame()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.sort()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
