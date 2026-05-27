/** Performs shallow client-side validation of youtube URL validity.
 * Can be bypassed, backend must also perform validation.
 * 
 * Citation (5/20):
 * https://regexr.com/
 */
import {ALLOWED_LINKS} from "../config/uploadConfig";


export function isValidYoutubeLink(link) {
    // Checks if the supplied link is from an allowed domain
    if (!link) return false;
    return (ALLOWED_LINKS.some(domain => link.includes(domain)));
};