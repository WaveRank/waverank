import { MAX_CONTENT_SIZE } from "../config/uploadConfig";

/** Converts a file size from bytes to a human-readable megabyte string. */
export function formatMB(bytes, precision=2) {
    return (bytes / (1024 * 1024)).toFixed(precision) + ' MB';
}

/** Checks if a file is within the defined size limit. */
export function isValidFileSize(file) {
    return file.size <= MAX_CONTENT_SIZE;
}