/** Performs shallow client-side validation of MIME type and extension.
 * Can be bypassed, backend must also perform validation.
 */
import { ALLOWED_EXTENSIONS, ALLOWED_TYPES } from "../config/uploadConfig";


export function isValidFileType(file) {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    return (
        ALLOWED_EXTENSIONS.includes(ext) 
        && ALLOWED_TYPES.includes(file.type) 
    );
};