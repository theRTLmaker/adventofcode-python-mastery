# progress_bar.py


def progress_bar(current, total, bar_length=30):
    """
    Displays or updates a progress bar in the terminal only when the integer
    percentage of progress changes. If progress reaches completion, it replaces '\r' with '\p'.

    Args:
        current (int): The current progress (e.g., the current loop iteration).
        total (int): The total amount of work (e.g., the length of the iterable).
        bar_length (int): The length of the progress bar in characters (default: 30).
    """
    # Calculate the progress percentage as an integer
    percentage = int((current / total) * 100)

    # Check if the progress percentage has changed
    if current == 1 or percentage != progress_bar.last_percentage:
        progress_bar.last_percentage = percentage  # Update the last percentage
        progress = current / total
        bar = "#" * int(progress * bar_length) + "-" * (
            bar_length - int(progress * bar_length))

        # Handle the 100% progress edge case differently
        if current == total:
            print(f"[{bar}] {percentage}%",
                  end="\n")  # Print with '\p' when 100% is reached
        else:
            print(f"[{bar}] {percentage}%", end="\r")


# Initialize a tracking attribute on the function
progress_bar.last_percentage = -1
