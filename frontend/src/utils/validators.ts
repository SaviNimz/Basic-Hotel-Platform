export interface ValidationResult<T> {
    value: T | null;
    error: string | null;
}


export function parseFloatValue(value: string, fieldName: string): ValidationResult<number> {
    const parsed = parseFloat(value);
    if (isNaN(parsed)) {
        return {
            value: null,
            error: `Please enter a valid ${fieldName}`,
        };
    }
    return {
        value: parsed,
        error: null,
    };
}


export function parsePositiveFloat(value: string, fieldName: string): ValidationResult<number> {
    const result = parseFloatValue(value, fieldName);
    if (result.value !== null && result.value <= 0) {
        return {
            value: null,
            error: `Please enter a valid ${fieldName} greater than 0`,
        };
    }
    return result;
}
