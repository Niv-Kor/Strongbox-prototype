def nthIndex(string, substring, n):
    parts = string.split(substring, n + 1)

    if len(parts) <= n + 1:
        return -1
    else:
        return len(string) - len(parts[-1]) - len(substring)
