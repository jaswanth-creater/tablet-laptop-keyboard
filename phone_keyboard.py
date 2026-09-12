from flask import Flask, request
from pynput.keyboard import Controller, Key

app = Flask(__name__)
keyboard = Controller()

SPECIAL_KEYS = {
    "esc": Key.esc,

    "f1": Key.f1,
    "f2": Key.f2,
    "f3": Key.f3,
    "f4": Key.f4,
    "f5": Key.f5,
    "f6": Key.f6,
    "f7": Key.f7,
    "f8": Key.f8,
    "f9": Key.f9,
    "f10": Key.f10,
    "f11": Key.f11,
    "f12": Key.f12,

    "tab": Key.tab,
    "caps": Key.caps_lock,
    "shift": Key.shift,
    "ctrl": Key.ctrl,
    "alt": Key.alt,
    "win": Key.cmd,

    "backspace": Key.backspace,
    "enter": Key.enter,
    "space": Key.space,

    "insert": Key.insert,
    "delete": Key.delete,
    "home": Key.home,
    "end": Key.end,
    "pageup": Key.page_up,
    "pagedown": Key.page_down,

    "up": Key.up,
    "down": Key.down,
    "left": Key.left,
    "right": Key.right,
}


HTML = r"""
<!DOCTYPE html>
<html>

<head>

<meta name="viewport"
      content="width=device-width,
               initial-scale=1.0,
               maximum-scale=1.0,
               user-scalable=no">

<title>RGB Laptop Keyboard</title>


<style>

/* =========================================
   RESET
   ========================================= */

* {
    box-sizing: border-box;

    -webkit-user-select: none;
    user-select: none;

    -webkit-touch-callout: none;
}

html,
body {

    margin: 0;
    padding: 0;

    width: 100%;
    height: 100%;

    overflow: hidden;

    background: #030303;
}

body {

    font-family: Arial, sans-serif;

    touch-action: none;
}


/* =========================================
   KEYBOARD
   ========================================= */

.keyboard {

    width: 100%;
    height: 100vh;

    padding: 7px;

    display: flex;
    flex-direction: column;

    gap: 5px;

    background: #030303;

    position: relative;

    overflow: hidden;
}


/* =========================================
   ROW
   ========================================= */

.row {

    flex: 1;

    display: flex;

    gap: 5px;

    min-height: 0;
}


/* =========================================
   NORMAL KEY
   ========================================= */

.key {

    flex: 1;

    min-width: 0;

    border: none;

    border-radius: 7px;

    position: relative;

    overflow: hidden;

    isolation: isolate;

    background:
        linear-gradient(
            145deg,
            #292929,
            #111111
        );

    color: rgba(255,255,255,0.95);

    font-size: clamp(
        11px,
        1.7vw,
        20px
    );

    font-weight: bold;

    display: flex;

    align-items: center;
    justify-content: center;

    box-shadow:

        inset 0 1px 2px
        rgba(255,255,255,0.12),

        inset 0 -3px 4px
        rgba(0,0,0,0.9),

        0 2px 4px
        rgba(0,0,0,0.8);

    transition:
        transform 0.04s,
        box-shadow 0.12s,
        background 0.12s;

    touch-action: none;

    text-shadow:

        0 0 2px #ffffff,

        0 0 4px
        var(--rgb),

        0 0 8px
        var(--rgb);
}


/* =========================================
   RGB UNDER EACH KEY
   ========================================= */

.key::before {

    content: "";

    position: absolute;

    left: -15%;
    right: -15%;

    bottom: -17px;

    height: 40px;

    border-radius: 50%;

    background:
        radial-gradient(
            ellipse,
            var(--rgb) 0%,
            transparent 70%
        );

    filter: blur(7px);

    opacity: 0.95;

    z-index: -2;

    pointer-events: none;
}


/* =========================================
   RGB SIDE LIGHT LEAK
   ========================================= */

.key::after {

    content: "";

    position: absolute;

    inset: 1px;

    border-radius: 6px;

    box-shadow:

        inset 0 0 5px
        var(--rgb),

        inset 0 -5px 9px
        var(--rgb);

    opacity: 0.40;

    z-index: -1;

    pointer-events: none;
}


/* =========================================
   RGB OFF MODE
   ========================================= */

.keyboard.rgb-off .key {

    --rgb: transparent;

    text-shadow: none;

    box-shadow:

        inset 0 1px 2px
        rgba(255,255,255,0.12),

        inset 0 -3px 4px
        rgba(0,0,0,0.9),

        0 2px 4px
        rgba(0,0,0,0.8);
}

.keyboard.rgb-off .key::before {

    opacity: 0;
}

.keyboard.rgb-off .key::after {

    opacity: 0;
}


/* =========================================
   PRESSED KEY
   ========================================= */

.key.pressed {

    transform: translateY(2px);

    background:
        linear-gradient(
            145deg,
            #303030,
            #080808
        );

    box-shadow:

        inset 0 0 8px
        var(--rgb),

        inset 0 -3px 5px
        rgba(0,0,0,0.9),

        0 0 7px
        var(--rgb),

        0 0 16px
        var(--rgb);
}


/* =========================================
   KEY TYPES
   ========================================= */

.function {

    font-size: clamp(
        10px,
        1.5vw,
        17px
    );
}

.modifier {

    font-size: clamp(
        10px,
        1.5vw,
        17px
    );
}

.special {

    font-size: clamp(
        10px,
        1.5vw,
        17px
    );
}


/* =========================================
   SPECIAL WIDTHS
   ========================================= */

.tab {
    flex: 1.45;
}

.caps {
    flex: 1.75;
}

.shift {
    flex: 2.15;
}

.backspace {
    flex: 2;
}

.enter {
    flex: 2;
}

.space {
    flex: 5;
}

.small-mod {
    flex: 1.15;
}

.nav-key {
    flex: 1.15;
}


/* =========================================
   SYMBOL KEYS
   ========================================= */

.symbol-key {

    flex-direction: column;

    line-height: 1;

    padding-top: 2px;
}

.shift-symbol {

    font-size: 0.72em;

    opacity: 0.95;

    margin-bottom: 2px;

    text-shadow:

        0 0 2px #ffffff,

        0 0 5px var(--rgb),

        0 0 8px var(--rgb);
}

.normal-symbol {

    font-size: 1em;

    text-shadow:

        0 0 2px #ffffff,

        0 0 5px var(--rgb),

        0 0 9px var(--rgb);
}


/* =========================================
   ARROW AREA
   ========================================= */

.arrow-area {

    flex: 2.8;

    display: flex;

    flex-direction: column;

    gap: 5px;
}

.arrow-top,
.arrow-bottom {

    flex: 1;

    display: flex;

    gap: 5px;
}

.arrow-key {
    flex: 1;
}


/* =========================================
   SPACER
   ========================================= */

.spacer {
    flex: 1;
}


/* =========================================
   RGB BUTTON
   ========================================= */

.rgb-control {

    flex: 1.15;

    border: none;

    border-radius: 7px;

    background:
        linear-gradient(
            145deg,
            #181818,
            #080808
        );

    color: white;

    font-size: clamp(
        10px,
        1.5vw,
        16px
    );

    font-weight: bold;

    position: relative;

    overflow: hidden;

    box-shadow:

        inset 0 1px 2px
        rgba(255,255,255,0.12),

        inset 0 -2px 3px
        rgba(0,0,0,0.8),

        0 2px 4px
        rgba(0,0,0,0.7);

    touch-action: none;

    z-index: 5;
}


.rgb-control::before {

    content: "";

    position: absolute;

    inset: -5px;

    background:
        linear-gradient(
            90deg,
            red,
            yellow,
            lime,
            cyan,
            blue,
            magenta,
            red
        );

    background-size: 400% 100%;

    animation:
        rgbButton 4s linear infinite;

    opacity: 0.7;

    filter: blur(5px);

    z-index: -1;
}

@keyframes rgbButton {

    0% {
        background-position: 0% 50%;
    }

    100% {
        background-position: 400% 50%;
    }
}


/* =========================================
   RGB BUTTON OFF
   ========================================= */

.rgb-control.off {

    color: #888;

    background:
        linear-gradient(
            145deg,
            #181818,
            #080808
        );
}

.rgb-control.off::before {

    display: none;
}


/* =========================================
   SYMBOL GLOW
   ========================================= */

.keyboard.rgb-off
.shift-symbol,
.keyboard.rgb-off
.normal-symbol {

    text-shadow: none;
}

</style>

</head>


<body>


<div class="keyboard" id="keyboard">


<!-- =====================================
     TOP NAVIGATION
     ===================================== -->

<div class="row">

<button class="key special nav-key"
        data-key="insert">

    Insert

</button>

<button class="key special nav-key"
        data-key="delete">

    Delete

</button>

<button class="key special nav-key"
        data-key="home">

    Home

</button>

<button class="key special nav-key"
        data-key="end">

    End

</button>

<button class="key special nav-key"
        data-key="pageup">

    PgUp

</button>

<button class="key special nav-key"
        data-key="pagedown">

    PgDn

</button>


<div class="spacer"></div>


<button
    class="rgb-control"
    id="rgbButton">

    RGB ON

</button>


</div>


<!-- =====================================
     FUNCTION ROW
     ===================================== -->

<div class="row">

<button class="key function"
        data-key="esc">

    Esc

</button>

<button class="key function"
        data-key="f1">F1</button>

<button class="key function"
        data-key="f2">F2</button>

<button class="key function"
        data-key="f3">F3</button>

<button class="key function"
        data-key="f4">F4</button>

<button class="key function"
        data-key="f5">F5</button>

<button class="key function"
        data-key="f6">F6</button>

<button class="key function"
        data-key="f7">F7</button>

<button class="key function"
        data-key="f8">F8</button>

<button class="key function"
        data-key="f9">F9</button>

<button class="key function"
        data-key="f10">F10</button>

<button class="key function"
        data-key="f11">F11</button>

<button class="key function"
        data-key="f12">F12</button>

</div>


<!-- =====================================
     NUMBER ROW
     ===================================== -->

<div class="row">

<button class="key symbol-key"
        data-char="`">

    <span class="shift-symbol">~</span>
    <span class="normal-symbol">`</span>

</button>

<button class="key symbol-key"
        data-char="1">

    <span class="shift-symbol">!</span>
    <span class="normal-symbol">1</span>

</button>

<button class="key symbol-key"
        data-char="2">

    <span class="shift-symbol">@</span>
    <span class="normal-symbol">2</span>

</button>

<button class="key symbol-key"
        data-char="3">

    <span class="shift-symbol">#</span>
    <span class="normal-symbol">3</span>

</button>

<button class="key symbol-key"
        data-char="4">

    <span class="shift-symbol">$</span>
    <span class="normal-symbol">4</span>

</button>

<button class="key symbol-key"
        data-char="5">

    <span class="shift-symbol">%</span>
    <span class="normal-symbol">5</span>

</button>

<button class="key symbol-key"
        data-char="6">

    <span class="shift-symbol">^</span>
    <span class="normal-symbol">6</span>

</button>

<button class="key symbol-key"
        data-char="7">

    <span class="shift-symbol">&amp;</span>
    <span class="normal-symbol">7</span>

</button>

<button class="key symbol-key"
        data-char="8">

    <span class="shift-symbol">*</span>
    <span class="normal-symbol">8</span>

</button>

<button class="key symbol-key"
        data-char="9">

    <span class="shift-symbol">(</span>
    <span class="normal-symbol">9</span>

</button>

<button class="key symbol-key"
        data-char="0">

    <span class="shift-symbol">)</span>
    <span class="normal-symbol">0</span>

</button>

<button class="key symbol-key"
        data-char="-">

    <span class="shift-symbol">_</span>
    <span class="normal-symbol">-</span>

</button>

<button class="key symbol-key"
        data-char="=">

    <span class="shift-symbol">+</span>
    <span class="normal-symbol">=</span>

</button>

<button class="key special backspace"
        data-key="backspace">

    Backspace

</button>

</div>


<!-- =====================================
     QWERTY ROW
     ===================================== -->

<div class="row">

<button class="key special tab"
        data-key="tab">

    Tab

</button>

<button class="key" data-char="q">Q</button>
<button class="key" data-char="w">W</button>
<button class="key" data-char="e">E</button>
<button class="key" data-char="r">R</button>
<button class="key" data-char="t">T</button>
<button class="key" data-char="y">Y</button>
<button class="key" data-char="u">U</button>
<button class="key" data-char="i">I</button>
<button class="key" data-char="o">O</button>
<button class="key" data-char="p">P</button>


<button class="key symbol-key"
        data-char="[">

    <span class="shift-symbol">{</span>
    <span class="normal-symbol">[</span>

</button>


<button class="key symbol-key"
        data-char="]">

    <span class="shift-symbol">}</span>
    <span class="normal-symbol">]</span>

</button>


<button class="key symbol-key"
        data-char="\">

    <span class="shift-symbol">|</span>
    <span class="normal-symbol">\</span>

</button>

</div>


<!-- =====================================
     HOME ROW
     ===================================== -->

<div class="row">

<button class="key special caps"
        data-key="caps">

    Caps Lock

</button>

<button class="key" data-char="a">A</button>
<button class="key" data-char="s">S</button>
<button class="key" data-char="d">D</button>
<button class="key" data-char="f">F</button>
<button class="key" data-char="g">G</button>
<button class="key" data-char="h">H</button>
<button class="key" data-char="j">J</button>
<button class="key" data-char="k">K</button>
<button class="key" data-char="l">L</button>


<button class="key symbol-key"
        data-char=";">

    <span class="shift-symbol">:</span>
    <span class="normal-symbol">;</span>

</button>


<button class="key symbol-key"
        data-char="'">

    <span class="shift-symbol">"</span>
    <span class="normal-symbol">'</span>

</button>


<button class="key special enter"
        data-key="enter">

    Enter

</button>

</div>


<!-- =====================================
     SHIFT ROW
     ===================================== -->

<div class="row">

<button class="key special shift"
        data-key="shift">

    Shift

</button>

<button class="key" data-char="z">Z</button>
<button class="key" data-char="x">X</button>
<button class="key" data-char="c">C</button>
<button class="key" data-char="v">V</button>
<button class="key" data-char="b">B</button>
<button class="key" data-char="n">N</button>
<button class="key" data-char="m">M</button>


<button class="key symbol-key"
        data-char=",">

    <span class="shift-symbol">&lt;</span>
    <span class="normal-symbol">,</span>

</button>


<button class="key symbol-key"
        data-char=".">

    <span class="shift-symbol">&gt;</span>
    <span class="normal-symbol">.</span>

</button>


<button class="key symbol-key"
        data-char="/">

    <span class="shift-symbol">?</span>
    <span class="normal-symbol">/</span>

</button>


<button class="key special shift"
        data-key="shift">

    Shift

</button>

</div>


<!-- =====================================
     BOTTOM ROW
     ===================================== -->

<div class="row">

<button class="key special small-mod"
        data-key="ctrl">

    Ctrl

</button>

<button class="key special small-mod"
        data-key="win">

    Win

</button>

<button class="key special small-mod"
        data-key="alt">

    Alt

</button>


<button class="key special space"
        data-key="space">

    SPACE

</button>


<button class="key special small-mod"
        data-key="alt">

    Alt

</button>

<button class="key special small-mod"
        data-key="ctrl">

    Ctrl

</button>


<div class="arrow-area">

    <div class="arrow-top">

        <button class="key special arrow-key"
                data-key="up">

            ↑

        </button>

    </div>


    <div class="arrow-bottom">

        <button class="key special arrow-key"
                data-key="left">

            ←

        </button>

        <button class="key special arrow-key"
                data-key="down">

            ↓

        </button>

        <button class="key special arrow-key"
                data-key="right">

            →

        </button>

    </div>

</div>

</div>


</div>


<script>

/* =========================================
   RGB
   ========================================= */

const keyboardArea =
    document.getElementById("keyboard");

const rgbButton =
    document.getElementById("rgbButton");

const keys =
    document.querySelectorAll(".key");


let rgbEnabled = true;

let rgbOffset = 0;


/*
   Give each key a slightly different
   position in the rainbow.
*/

keys.forEach((key, index) => {

    const hue =
        (index * 17) % 360;

    key.style.setProperty(
        "--rgb",
        `hsl(${hue}, 100%, 55%)`
    );

});


/*
   Smooth RGB movement.
*/

function updateRGB() {

    if (rgbEnabled) {

        rgbOffset += 0.35;


        keys.forEach(
            (key, index) => {

                const hue =
                    (
                        index * 17 +
                        rgbOffset
                    ) % 360;


                key.style.setProperty(
                    "--rgb",
                    `hsl(${hue}, 100%, 55%)`
                );

            }
        );
    }


    requestAnimationFrame(
        updateRGB
    );
}


updateRGB();


/* =========================================
   RGB ON / OFF
   ========================================= */

rgbButton.addEventListener(
    "pointerdown",
    event => {

        event.preventDefault();

        event.stopPropagation();


        rgbEnabled =
            !rgbEnabled;


        if (rgbEnabled) {

            keyboardArea.classList.remove(
                "rgb-off"
            );

            rgbButton.textContent =
                "RGB ON";

            rgbButton.classList.remove(
                "off"
            );

        }

        else {

            keyboardArea.classList.add(
                "rgb-off"
            );

            rgbButton.textContent =
                "RGB OFF";

            rgbButton.classList.add(
                "off"
            );
        }
    }
);


/* =========================================
   AUDIO
   ========================================= */

let audioContext = null;


function initAudio() {

    if (!audioContext) {

        audioContext =
            new (
                window.AudioContext ||
                window.webkitAudioContext
            )();
    }


    if (
        audioContext.state ===
        "suspended"
    ) {

        audioContext.resume();
    }
}


function keySound(type) {

    initAudio();


    const oscillator =
        audioContext.createOscillator();


    const gain =
        audioContext.createGain();


    oscillator.type =
        "square";


    let frequency = 850;

    let volume = 0.075;

    let duration = 0.045;


    if (type === "space") {

        frequency = 180;

        volume = 0.11;

        duration = 0.065;

    }

    else if (type === "enter") {

        frequency = 220;

        volume = 0.105;

        duration = 0.06;

    }

    else if (type === "modifier") {

        frequency = 650;

        volume = 0.09;

        duration = 0.045;
    }


    oscillator.frequency.value =
        frequency;


    gain.gain.setValueAtTime(
        volume,
        audioContext.currentTime
    );


    gain.gain.exponentialRampToValueAtTime(
        0.001,
        audioContext.currentTime +
        duration
    );


    oscillator.connect(gain);

    gain.connect(
        audioContext.destination
    );


    oscillator.start();


    oscillator.stop(
        audioContext.currentTime +
        duration
    );
}


/* =========================================
   SOUND TYPE
   ========================================= */

function getSoundType(key) {

    if (key === "space")
        return "space";


    if (key === "enter")
        return "enter";


    if (

        key === "ctrl" ||

        key === "shift" ||

        key === "alt" ||

        key === "win"

    )

        return "modifier";


    return "normal";
}


/* =========================================
   SEND KEY
   ========================================= */

function send(
    action,
    key,
    char = ""
) {

    fetch(
        "/key",
        {

            method: "POST",

            headers: {

                "Content-Type":
                    "application/json"

            },

            body: JSON.stringify({

                action: action,

                key: key,

                char: char

            })

        }
    ).catch(() => {});
}


/* =========================================
   PRESS KEY
   ========================================= */

function pressKey(element) {

    if (
        element.classList.contains(
            "pressed"
        )
    )

        return;


    element.classList.add(
        "pressed"
    );


    const key =
        element.dataset.key;


    const char =
        element.dataset.char;


    if (char !== undefined) {

        keySound("normal");

        send(
            "char",
            "",
            char
        );

        return;
    }


    if (key) {

        keySound(
            getSoundType(key)
        );


        if (

            key === "ctrl" ||

            key === "shift" ||

            key === "alt" ||

            key === "win"

        ) {

            send(
                "press",
                key
            );

        }

        else {

            send(
                "tap",
                key
            );
        }
    }
}


/* =========================================
   RELEASE KEY
   ========================================= */

function releaseKey(element) {

    if (
        !element.classList.contains(
            "pressed"
        )
    )

        return;


    element.classList.remove(
        "pressed"
    );


    const key =
        element.dataset.key;


    if (!key)
        return;


    if (

        key === "ctrl" ||

        key === "shift" ||

        key === "alt" ||

        key === "win"

    ) {

        send(
            "release",
            key
        );
    }
}


/* =========================================
   TOUCH / POINTER
   ========================================= */

keys.forEach(key => {


    key.addEventListener(
        "pointerdown",
        event => {

            event.preventDefault();

            initAudio();


            try {

                key.setPointerCapture(
                    event.pointerId
                );

            }

            catch(e) {}


            pressKey(key);
        }
    );


    key.addEventListener(
        "pointerup",
        event => {

            event.preventDefault();

            releaseKey(key);
        }
    );


    key.addEventListener(
        "pointercancel",
        event => {

            event.preventDefault();

            releaseKey(key);
        }
    );


    key.addEventListener(
        "contextmenu",
        event => {

            event.preventDefault();

            return false;
        }
    );


    key.addEventListener(
        "dragstart",
        event => {

            event.preventDefault();

            return false;
        }
    );

});


/* =========================================
   PREVENT LONG PRESS MENU
   ========================================= */

document.addEventListener(
    "contextmenu",
    event =>
        event.preventDefault()
);


document.addEventListener(
    "selectstart",
    event =>
        event.preventDefault()
);


document.addEventListener(
    "dragstart",
    event =>
        event.preventDefault()
);

</script>


</body>
</html>
"""


@app.route("/")
def index():

    return HTML


@app.route(
    "/key",
    methods=["POST"]
)
def key_event():

    data = request.get_json()

    action = data.get("action")

    key_name = data.get("key")

    char = data.get("char")


    try:

        if action == "char":

            if char:

                keyboard.press(char)

                keyboard.release(char)


        elif action == "tap":

            key = SPECIAL_KEYS.get(
                key_name
            )

            if key:

                keyboard.press(key)

                keyboard.release(key)


        elif action == "press":

            key = SPECIAL_KEYS.get(
                key_name
            )

            if key:

                keyboard.press(key)


        elif action == "release":

            key = SPECIAL_KEYS.get(
                key_name
            )

            if key:

                keyboard.release(key)


        return {
            "status": "ok"
        }


    except Exception as e:

        return {

            "status": "error",

            "message": str(e)

        }, 500


if __name__ == "__main__":

    print()
    print(
        "===================================="
    )
    print(
        "     RGB TABLET LAPTOP KEYBOARD"
    )
    print(
        "===================================="
    )
    print()

    print(
        "Open on Galaxy Tab:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print()


    app.run(
        host="127.0.0.1",
        port=5000
    )