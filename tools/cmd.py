# Allowlist of permitted base commands. Only commands whose first token appears
# in this set will be executed — everything else is blocked by default.
# Adjust this list to match the exact capabilities your use case requires.
ALLOWED_COMMANDS = (
    # Filesystem navigation & inspection
    "ls",       # List directory contents
    "cat",      # Print file contents
    "head",     # Print first N lines of a file
    "tail",     # Print last N lines of a file
    "pwd",      # Print working directory
    "find",     # Search for files by name, type, size, etc.
    "du",       # Disk usage of files/directories
    "df",       # Free disk space on mounted filesystems
    "stat",     # Detailed metadata about a file (size, permissions, timestamps)
    "file",     # Detect file type from content (not just extension)
    "wc",       # Word/line/character count
    # Text processing
    "grep",     # Search file contents by pattern
    "awk",      # Column-oriented text processing
    "sed",      # Stream editor for substitutions and transforms
    "sort",     # Sort lines of text
    "uniq",     # Remove or count duplicate lines
    "cut",      # Extract columns from delimited text
    "tr",       # Translate or delete characters
    "diff",     # Compare two files line by line
    # System information (read-only)
    "echo",     # Print a string (useful for testing/debugging)
    "date",     # Current date and time
    "uptime",   # How long the system has been running
    "whoami",   # Current username
    "uname",    # OS/kernel information
    "ps",       # Snapshot of running processes
    "env",      # Print environment variables
    "which",    # Locate a command on PATH
    "lsof",     # List open files and the processes using them
)
