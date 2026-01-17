/**
 * Parses error details from API responses
 * Handles both string and array formats returned by FastAPI
 */
export function parseErrorDetail(detail: any): string {
    if (typeof detail === 'string') {
        return detail;
    }
    if (Array.isArray(detail)) {
        return detail.map((e: any) => e.msg).join(', ');
    }
    return 'An unexpected error occurred';
}

/**
 * Extracts error message from API error response
 * Provides a fallback message if the error format is unexpected
 * 
 * @param err - The error object from axios/API call
 * @param fallback - The fallback message if error details cannot be extracted
 * @returns The error message to display to the user
 */
export function extractErrorMessage(err: any, fallback: string): string {
    const detail = err.response?.data?.detail;
    if (detail !== undefined) {
        return parseErrorDetail(detail);
    }
    return fallback;
}
