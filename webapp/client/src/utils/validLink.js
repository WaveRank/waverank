/** Performs shallow client-side validation of youtube URL validity.
 * Can be bypassed, backend must also perform validation.
 * 
 * Citation (5/20):
 * https://regexr.com/
 */
import {ALLOWED_LINKS} from "../config/uploadConfig";


export function isValidYoutubeLink(link) {
    if (!link) return false;
    // (= or /) (11 alphanum) (end of link or & or ?)
    const regex = /([=/])\w{11}($|[&?])/;
    return (
        ALLOWED_LINKS.some(domain => link.includes(domain))
        && regex.test(link)
    );
};