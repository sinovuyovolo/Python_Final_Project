document.addEventListener('DOMContentLoaded', () => {

    // Demo global variables
    const demoUserId = 'demo-user-123';
    let displayName = "Snow"; // Placeholder name

    // --- UI Element References ---
    const display = document.getElementById('display');
    const calculatorScreen = document.getElementById('calculator-screen');
    const mainApp = document.getElementById('main-app');
    const themeToggle = document.getElementById('theme-toggle');
    const languageSelector = document.getElementById('language-selector');
    const navButtons = document.querySelectorAll('aside button');
    const sosButton = document.getElementById('sos-button');
    const modalContainer = document.getElementById('modal-container');
    const modalTitle = document.getElementById('modal-title');
    const modalMessage = document.getElementById('modal-message');
    const modalButtons = document.getElementById('modal-buttons');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const profileForm = document.getElementById('profile-form');
    const saveJournalBtn = document.getElementById('save-journal-btn');
    const journalEntriesList = document.getElementById('journal-entries');
    const calcButtons = document.querySelectorAll('.calculator .btn');
    const authStatus = document.getElementById('auth-status');

    let currentInput = '';
    let isResultDisplayed = false;

    // --- Calculator Logic ---
    calcButtons.forEach(button => {
        button.addEventListener('click', () => {
            const value = button.dataset.value;
            if (value === 'C') {
                clearDisplay();
            } else if (value === '=') {
                calculate();
            } else {
                appendToDisplay(value);
            }
        });
    });

    function appendToDisplay(value) {
        if (isResultDisplayed || display.innerText === '0') {
            display.innerText = '';
            isResultDisplayed = false;
        }
        display.innerText += value;
    }

    function clearDisplay() {
        display.innerText = '0';
        isResultDisplayed = false;
    }

    /**
     * Attempts to perform a calculation or calls the backend API to check the code.
     */
    async function calculate() {
        currentInput = display.innerText;
        // Regex to check if the input is only digits (potential secret code)
        if (currentInput.match(/^\d+$/)) {
            try {
                // IMPORTANT: This calls the Vercel Serverless Function endpoint
                const response = await fetch('/api/check_code', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ code: currentInput })
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    unlockApp();
                } else {
                    display.innerText = 'Invalid Code';
                    isResultDisplayed = true;
                    authStatus.innerText = 'Incorrect PIN. Try 1234';
                    setTimeout(() => authStatus.innerText = '', 3000);
                }
            } catch (error) {
                console.error('API Error:', error);
                authStatus.innerText = 'Error connecting to the shield server.';
            }
        } else {
            // Normal calculator logic for expressions like 5+3
            try {
                // Note: Use of eval is discouraged in production but used here for simple demo calculator functionality
                const result = eval(currentInput);
                display.innerText = result;
                isResultDisplayed = true;
            } catch (error) {
                display.innerText = 'Error';
                isResultDisplayed = true;
            }
        }
    }

    function unlockApp() {
        calculatorScreen.classList.add('hidden');
        mainApp.classList.remove('hidden');
        updateUI();
        startChatbot();
        loadDemoData();
    }

    // --- Theme Toggle ---
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark');
        themeToggle.classList.toggle('dark');
    });

    // --- Language Selector & Translations ---
    const translations = {
        en: {
            greeting: "Hello, " + displayName + "!", wellnessPrompt: "How are you feeling today?", sos: "SOS",
            confirmSos: "Are you sure? This will simulate contacting emergency services.", confirm: "Confirm",
            cancel: "Cancel", dispatching: "Police & Ambulance Dispatched to [Your Saved Address]. ETA: 8 Minutes.",
            contactsTitle: "Emergency Contacts", dateTitle: "On a Date", journalTitle: "Private Journal",
            saslTitle: "Sign Language & Emoji Key", profileTitle: "My Information",
        },
        zu: {
            greeting: "Sawubona, " + displayName + "!", wellnessPrompt: "Uzwani namuhla?", sos: "SOS",
            confirmSos: "Uqinisekile? Lokhu kuzoxhumana nezinsizakalo eziphuthumayo.", confirm: "Qinisekisa",
            cancel: "Khansela", dispatching: "Amaphoyisa kanye ne-Ambulance Bathunyelwe e- [Ikheli lakho Elilondoloziwe]. ETA: 8 Minutes.",
            contactsTitle: "Oxhumana Nabo Abaphuthumayo", dateTitle: "Usuku Oluphephile", journalTitle: "Ijenali Eyimfihlo",
            saslTitle: "Ulimi Lwezandla & Okhiye Bezithonjana", profileTitle: "Imininingwane Yami",
        },
        xh: {
            greeting: "Molo, " + displayName + "!", wellnessPrompt: "Unjani namhlanje?", sos: "SOS",
            confirmSos: "Uqinisekile? Oku kuza kunxibelelanisa iinkonzo ezingxamisekileyo.", confirm: "Qinisekisa",
            cancel: "Rhoxisa", dispatching: "Amapolisa kunye ne-Ambulance Zithunyelwe ku- [Idilesi yakho Egcinwe]. ETA: 8 Imizuzu.",
            contactsTitle: "Abafowunelwa Abangxamisekileyo", dateTitle: "Usuku Olukhuselekileyo", journalTitle: "Ijenali Yabucala",
            saslTitle: "Ulimi Lweempawu kunye Nesitshixo Se-Emoji", profileTitle: "Ulwazi Lwam",
        },
        af: {
            greeting: "Hallo, " + displayName + "!", wellnessPrompt: "Hoe voel jy vandag?", sos: "SOS",
            confirmSos: "Is jy seker? Dit sal nooddienste kontak.", confirm: "Bevestig",
            cancel: "Kanselleer", dispatching: "Polisie & Ambulans is na [Jou Gestoorde Adres] gestuur. ETA: 8 Minute.",
            contactsTitle: "Noodkontakte", dateTitle: "Datum Veiligheid", journalTitle: "Privaatjoernaal",
            saslTitle: "Gebaretaal & Emoji Sleutel", profileTitle: "My Inligting",
        },
        ss: {
            greeting: "Sawubona, " + displayName + "!", wellnessPrompt: "Unjani namuhla?", sos: "SOS",
            confirmSos: "Ucinisile? Loku kutakucocisana netinsito letiphutfumako.", confirm: "Cinisekisa",
            cancel: "Khansela", dispatching: "Emaphoyisa kanye ne-Ambulance Batfumele e- [Likheli Lakho Lelilondoloziwe]. ETA: 8 Minutes.",
            contactsTitle: "Bocana Nabo Labaphutfumako", dateTitle: "Usuku Loluphephile", journalTitle: "Ijenali Eyimfihlo",
            saslTitle: "Lulwimi Lwetimpawu & Okhiye Be-Emoji", profileTitle: "Imininingwane Yami",
        },
        nr: {
            greeting: "Sawubona, " + displayName + "!", wellnessPrompt: "Uzwani namuhla?", sos: "SOS",
            confirmSos: "Uqinisekile? Lokhu kuzokuthintana nezinsizakalo eziphuthumayo.", confirm: "Qinisekisa",
            cancel: "Khansela", dispatching: "Amaphoyisa kanye ne-Ambulance Bathunyelwe e- [Ikheli lakho Elilondoloziwe]. ETA: 8 Minutes.",
            contactsTitle: "Oxhumana Nabo Abaphuthumayo", dateTitle: "Usuku Oluphephile", journalTitle: "Ijenali Eyimfihlo",
            saslTitle: "Ulimi Lwezandla & Okhiye Be-Emoji", profileTitle: "Imininingwane Yami",
        },
        st: {
            greeting: "Dumela, " + displayName + "!", wellnessPrompt: "Oho joale u ikutloa joang?", sos: "SOS",
            confirmSos: "Oa kholiseha? Sena se tla ikopanya le litšebeletso tsa tšohanyetso.", confirm: "Tiisa",
            cancel: "Hlakola", dispatching: "Mapolesa le Ambulanse Ba rometsoe ho [Aterese ea Hau e Bolokiloeng]. ETA: 8 Metsotso.",
            contactsTitle: "Batho Bao U ka Ikopanyang le Bona ka Tšohanyetso", dateTitle: "Letsatsi le Sireletsegileng", journalTitle: "Jenale ya Lekunutu",
            saslTitle: "Puo ya Matsoho le Senotlolo sa Emoji", profileTitle: "Tsebo ya Ka",
        },
        tn: {
            greeting: "Dumela, " + displayName + "!", wellnessPrompt: "O ikutlwa jang gompieno?", sos: "SOS",
            confirmSos: "O netefatsa? Se se tla ikgolaganya le ditirelo tsa tšoganetso.", confirm: "Netefatsa",
            cancel: "Hlakola", dispatching: "Mapodisi le Ambulanse ba rometswe kwa [Aterese ya Gago e Bolokilweng]. ETA: 8 Metsotso.",
            contactsTitle: "Ba Ikaganya ba Tšoganetso", dateTitle: "Letsatsi le Sireletsegileng", journalTitle: "Jenale ya Bosegogadi",
            saslTitle: "Puololelo ya Matshwao le Senotlolo sa Emoji", profileTitle: "Tshedimosetso ya Me",
        },
        ve: {
            greeting: "Ndaa, " + displayName + "!", wellnessPrompt: "U khou pfa hani namusi?", sos: "SOS",
            confirmSos: "Ni na n\u0334ango? Izwi lifana na la vhukuma.", confirm: "N\u0334eavhekhani",
            cancel: "Hengisa", dispatching: "Vhapolisa na Ambulanse Vho rwalelwa [Adiresi Yanu Yo Dzheniswa]. ETA: 8 Minetsi.",
            contactsTitle: "Vhukano Vha Vhukhakhani", dateTitle: "ḓuvha Ḽo Fukedzwaho", journalTitle: "Ḓivhadza Ḽa Mbudzi",
            saslTitle: "Ḽino la Mavhuli na Senzela Sa Emoji", profileTitle: "Mbudzi Yanga",
        },
        ts: {
            greeting: "Avuxeni, " + displayName + "!", wellnessPrompt: "U titwa njhani namuntlha?", sos: "SOS",
            confirmSos: "U na ntswa? Se swi ta vonakala.", confirm: "Ntwananiso",
            cancel: "Yisa", dispatching: "Vapolisi na Ambulense va rhumiwile eka [Adirese ya Wena Yo Fambisiwa]. ETA: 8 Minuta.",
            contactsTitle: "Mhaka Ya Vuhosi", dateTitle: "Lixaka Lele", journalTitle: "Vutomi Vanga",
            saslTitle: "Masungulo na Masungulo ya Mahungu", profileTitle: "Vutomi bya Mina",
        },
        nso: {
            greeting: "Dumela, " + displayName + "!", wellnessPrompt: "O ikgwa bjang lehono?", sos: "SOS",
            confirmSos: "O a duma? Se se tla ikopanya le ditirelo tsa tšohanyetso.", confirm: "Dumela",
            cancel: "Feta", dispatching: "Sepodisi le Ambulanse di rometswe go [Aterese ya Gago e Bolokilwego]. ETA: 8 Metsotso.",
            contactsTitle: "Dikamano tsa Tšohanyetso", dateTitle: "Letsatsi le Bolokilwego", journalTitle: "Jenale ya Lekunutu",
            saslTitle: "Puo ya Matsoho le Senotlolo sa Emoji", profileTitle: "Tsebo ya Ka",
        }
    };

    languageSelector.addEventListener('change', (event) => {
        const lang = event.target.value;
        localStorage.setItem('language', lang);
        updateUI();
    });

    function updateUI() {
        const lang = localStorage.getItem('language') || 'en';
        const text = translations[lang] || translations['en'];
        // Update name in translation object before setting text
        text.greeting = text.greeting.replace("Snow", displayName); 
        document.getElementById('greeting').innerText = text.greeting;
        document.getElementById('wellness-prompt').innerText = text.wellnessPrompt;
        document.getElementById('sos-button').innerText = text.sos;
    }

    // --- Navigation ---
    navButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.id.replace('nav-', '') + '-dashboard';
            showDashboard(targetId);
        });
    });

    function showDashboard(id) {
        const dashboards = document.querySelectorAll('.dashboard');
        dashboards.forEach(db => db.classList.add('hidden'));
        document.getElementById(id).classList.remove('hidden');

        // Always show the chatbot on the main dashboard screen for easy access
        if (id === 'main-dashboard') {
            document.getElementById('chatbot-screen').classList.remove('hidden');
        } else {
            document.getElementById('chatbot-screen').classList.add('hidden');
        }
    }

    // --- Modal Logic (for SOS and Alerts) ---
    function showModal(title, message, buttonsHtml) {
        modalTitle.innerText = title;
        modalMessage.innerText = message;
        modalButtons.innerHTML = buttonsHtml;
        modalContainer.classList.remove('hidden');
    }

    function hideModal() {
        modalContainer.classList.add('hidden');
    }

    // --- SOS Button Logic ---
    sosButton.addEventListener('click', () => {
        const lang = localStorage.getItem('language') || 'en';
        const text = translations[lang] || translations['en'];

        showModal(
            "Emergency Alert",
            text.confirmSos,
            `<button id="modal-confirm" class="px-6 py-2 rounded-xl bg-red-600 text-white hover:bg-red-700 transition-colors">${text.confirm}</button>` +
            `<button id="modal-cancel" class="px-6 py-2 rounded-xl bg-gray-400 text-gray-800 hover:bg-gray-500 transition-colors">${text.cancel}</button>`
        );
        document.getElementById('modal-confirm').addEventListener('click', () => {
            hideModal();
            showModal(
                "DISPATCHING",
                text.dispatching,
                '<button id="modal-ok" class="px-6 py-2 rounded-xl bg-emerald-500 text-white hover:bg-emerald-600 transition-colors">OK</button>'
            );
            document.getElementById('modal-ok').addEventListener('click', hideModal);
        });
        document.getElementById('modal-cancel').addEventListener('click', hideModal);
    });

    // --- Chatbot Logic ---
    function startChatbot() {
        appendMessage("Welcome! My name is iKhuselo. How can I assist you?", 'bot');
        appendMessage("Please tell me your name so I can address you correctly.", 'bot');
    }

    function sendMessage() {
        const message = chatInput.value.trim();
        if (message.length === 0) return;

        appendMessage(message, 'user');
        chatInput.value = '';

        let botResponse;
        if (message.toLowerCase().includes("name")) {
            botResponse = "My name is iKhuselo. It means 'digital shield' in isiXhosa.";
        } else if (message.toLowerCase().includes("how are you")) {
            botResponse = "I'm doing great, thank you for asking! How can I help you?";
        } else {
            botResponse = `Hello ${displayName}. That's an interesting thought. Remember to use the other features in the app!`;
        }

        setTimeout(() => appendMessage(botResponse, 'bot'), 1000);
    }

    function appendMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('p-3', 'rounded-xl', 'max-w-xs', 'break-words', 'shadow-sm');
        if (sender === 'user') {
            messageDiv.classList.add('bg-blue-500', 'text-white', 'self-end', 'ml-auto', 'rounded-br-none');
        } else {
            messageDiv.classList.add('bg-gray-300', 'dark:bg-gray-600', 'self-start', 'mr-auto', 'rounded-bl-none');
        }
        messageDiv.innerText = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    // --- Demo Data & Persistence Logic (Uses local data since we don't have Firestore/DB setup yet) ---
    function loadDemoData() {
        // Mock Profile Data
        const demoProfileData = {
            fullName: "Thando Nkosi",
            age: "28",
            address: "123 Freedom St, Johannesburg",
            allergies: "None",
            bloodType: "O+",
            userId: demoUserId,
        };
        // Update the display name
        displayName = demoProfileData.fullName; 

        // Populate Profile Form
        document.getElementById('profile-name').value = demoProfileData.fullName;
        document.getElementById('profile-age').value = demoProfileData.age;
        document.getElementById('profile-address').value = demoProfileData.address;
        document.getElementById('profile-allergies').value = demoProfileData.allergies;
        document.getElementById('profile-blood-type').value = demoProfileData.bloodType;

        // Mock Journal Data
        const demoJournalEntries = [
            { text: "My first entry in iKhuselo. I feel safe.", createdAt: new Date() },
            { text: "Had a great day out in the sun. Hope to write more often.", createdAt: new Date(Date.now() - 86400000) } // One day ago
        ];
        
        journalEntriesList.innerHTML = '';
        demoJournalEntries.forEach((entry) => {
            const entryDiv = document.createElement('div');
            entryDiv.classList.add('p-4', 'bg-gray-200', 'dark:bg-gray-600', 'rounded-lg', 'shadow-md');
            entryDiv.innerHTML = `<p>${entry.text}</p><p class="text-xs text-gray-500 mt-2">${entry.createdAt.toLocaleString()}</p>`;
            journalEntriesList.appendChild(entryDiv);
        });

        // Set user info placeholders
        document.getElementById('auth-info').innerText = `Demo User ID: ${demoUserId}`;
        document.getElementById('user-id-journal').innerText = `Your Journal ID: ${demoUserId}`;
        document.getElementById('user-id-profile').innerText = `Your Profile ID: ${demoUserId}`;

        updateUI(); // Final UI update with the user's name
    }

    // --- Demo Saving Alerts ---
    profileForm.addEventListener('submit', (e) => {
        e.preventDefault();
        showModal("Demo Mode", "Your profile information is not being saved in this demo. It will be reset when you refresh.", '<button id="modal-ok" class="px-6 py-2 rounded-xl bg-emerald-500 text-white hover:bg-emerald-600 transition-colors">OK</button>');
        document.getElementById('modal-ok').addEventListener('click', hideModal);
    });

    saveJournalBtn.addEventListener('click', () => {
        showModal("Demo Mode", "Your journal entry is not being saved in this demo. It will be reset when you refresh.", '<button id="modal-ok" class="px-6 py-2 rounded-xl bg-emerald-500 text-white hover:bg-emerald-600 transition-colors">OK</button>');
        document.getElementById('modal-ok').addEventListener('click', hideModal);
    });

    document.getElementById('date-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const timerInput = document.getElementById('date-timer').value;
        showModal("Demo Mode", `Timer set for ${timerInput} minutes. In a real app, this would notify contacts if you don't check in.`, '<button id="modal-ok" class="px-6 py-2 rounded-xl bg-emerald-500 text-white hover:bg-emerald-600 transition-colors">OK</button>');
        document.getElementById('modal-ok').addEventListener('click', hideModal);
    });
});
