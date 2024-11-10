function showSafety () {
    if (ifDanger == 1) {
        basic.showIcon(IconNames.Happy)
        music.stopAllSounds()
    } else if (ifDanger == 2) {
        basic.showIcon(IconNames.Asleep)
        music.stopAllSounds()
    } else if (ifDanger == 3 && ifDoorOpen != 2) {
        basic.showIcon(IconNames.Sad)
    } else if (ifDanger == 3 && ifDoorOpen == 2 && ifDoorLock == 1) {
        music.setVolume(255)
        basic.showIcon(IconNames.Sword)
        music.play(music.stringPlayable("A A - - A A - - ", 1240), music.PlaybackMode.InBackground)
    }
    if (ifDoorLock == 2) {
        music.stopAllSounds()
    }
    control.waitMicros(4000)
}
input.onButtonPressed(Button.A, function () {
    if (ifDoorOpen == 1) {
        if (ifDoorLock == 2) {
        	
        } else if (ifDoorLock == 1 && ifDanger == 1 || ifDoorLock == 1 && ifDanger == 2) {
            ifDoorOpen = 2
            olddoor = ifDoorOpen
            showOpen()
        } else if (ifDoorLock == 1 && ifDanger == 3) {
            music.setVolume(255)
            music.play(music.stringPlayable("A A - - A A - - ", 1240), music.PlaybackMode.InBackground)
            basic.showIcon(IconNames.Sword)
            ifDoorLock = 2
            oldlock = ifDoorLock
            showLock()
            music.stopAllSounds()
        }
    } else {
        ifDoorOpen = 1
        olddoor = ifDoorOpen
        showOpen()
    }
    serial.writeString("" + convertToText(ifDanger * 100 + ifDoorOpen * 10 + ifDoorLock) + "\n")
})
function showOpen () {
    if (ifDoorOpen == 1) {
        basic.showIcon(IconNames.SmallSquare)
    } else if (ifDoorOpen == 2) {
        basic.showIcon(IconNames.Square)
    }
    control.waitMicros(4000)
}
function showLock () {
    if (ifDoorLock == 1) {
        basic.showIcon(IconNames.Diamond)
    } else if (ifDoorLock == 2) {
        basic.showIcon(IconNames.SmallDiamond)
    }
    control.waitMicros(4000)
}
input.onButtonPressed(Button.B, function () {
    if (ifDoorLock == 2) {
        ifDoorLock = 1
    } else {
        ifDoorLock = 2
    }
    oldlock = ifDoorLock
    showLock()
    serial.writeString("" + convertToText(ifDanger * 100 + ifDoorOpen * 10 + ifDoorLock) + "\n")
})
let num = 0
let receivedString = ""
let oldlock = 0
let olddoor = 0
let ifDanger = 0
let ifDoorLock = 0
let ifDoorOpen = 0
serial.redirect(
SerialPin.USB_TX,
SerialPin.USB_RX,
BaudRate.BaudRate9600
)
radio.setGroup(12)
images.createImage(`
    . # . # .
    # . # . #
    # . . . #
    . # . # .
    . . # . .
    `).showImage(0)
ifDoorOpen = 1
ifDoorLock = 2
ifDanger = 1
olddoor = 1
oldlock = 2
// 4:关门
// 
// 5：开门
// 
// 6：解锁
// 
// 7：上锁
basic.forever(function () {
    receivedString = serial.readString()
    if (receivedString.length > 0) {
        num = parseFloat(receivedString)
        ifDanger = Math.floor(num / 100)
        ifDoorOpen = Math.floor(num % 100 / 10)
        ifDoorLock = num % 10
        if (olddoor != ifDoorOpen) {
            olddoor = ifDoorOpen
            showOpen()
        }
        if (oldlock != ifDoorLock) {
            oldlock = ifDoorLock
            showLock()
        }
        control.waitMicros(500000)
    }
    showSafety()
})
