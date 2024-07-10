#!/bin/bash

#create by chatGPT 3.5 openia

# Backup function
backup_directory() {
    source_dir="$1"
    backup_dir="$2"
    timestamp=$(date +%Y%m%d_%H%M%S)
    backup_file="${backup_dir}/backup_${timestamp}.tar.gz"

    if [ -d "$source_dir" ]; then
        echo "Creating backup of $source_dir to $backup_file..."
        tar -czf "$backup_file" "$source_dir"
        echo "Backup completed!"
        cleanup_backups "$backup_dir"
    else
        echo "Source directory $source_dir not found. Backup failed."
    fi
}

# Restore function
restore_backup() {
    source_dir="$1"
    backup_file="$2"

    if [ -d "$source_dir" ]; then
        echo "Restoring backup $backup_file to $source_dir..."
        tar -xzf "$backup_file" -C "$source_dir"
        echo "Restore completed!"
    else
        echo "Destination directory $source_dir not found. Restore failed."
    fi
}

# Cleanup old backups function
cleanup_backups() {
    backup_dir="$1"
    num_backups=$(ls "$backup_dir" | grep -c '^backup_.*\.tar\.gz$')
    max_backups=3

    if [ "$num_backups" -gt "$max_backups" ]; then
        echo "Cleaning up old backups..."
        ls -t "$backup_dir" | grep '^backup_.*\.tar\.gz$' | tail -n +"$((max_backups + 1))" | xargs -d '\n' rm -f
    fi
}

# Main script
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 [b <source_directory>] [r <destination_directory> <backup_file>]"
    exit 1
fi

case "$1" in
    b)
        source_directory="$2"
        backup_directory "$source_directory" "backups"
        ;;
    r)
        if [ "$#" -ne 4 ]; then
            echo "Invalid number of arguments for restore."
            exit 1
        fi
        destination_directory="$2"
        backup_file="$3"
        restore_backup "$destination_directory" "$backup_file"
        ;;
    *)
        echo "Invalid option. Usage: $0 [b <source_directory>] [r <destination_directory> <backup_file>]"
        exit 1
        ;;
esac
