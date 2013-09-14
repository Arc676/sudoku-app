import QtQuick 2.0
import Ubuntu.Components 0.1
import Ubuntu.Components.Popups 0.1

UbuntuShape {
    id: gameDifficultyButton
    property string buttonText
    color: sudokuBlocksGrid.dialogButtonColor2
    Image {
        source: "../icons/sudoku-vector-desktop.svg"
        anchors.fill: parent
        z:-1
    }

    Label {
        text: buttonText
        anchors.centerIn: parent
        color: sudokuBlocksGrid.dialogButtonTextColor
        opacity: 1
    }
    signal triggered;

    SequentialAnimation {
        id: animateDialogButton
        UbuntuNumberAnimation {
            id: animateDialogButton1
            target: gameDifficultyButton
            properties: "scale"
            to: 1.1
            from: 1
            duration: UbuntuAnimation.SnapDuration
            easing: UbuntuAnimation.StandardEasing
        }
        UbuntuNumberAnimation {
            id: animateDialogButton2
            target: gameDifficultyButton
            properties: "scale"
            to: 1
            from: 1.1
            duration: UbuntuAnimation.SnapDuration
            easing: UbuntuAnimation.StandardEasing
        }
        onRunningChanged: {
            if (animateDialogButton.running == false ) {
                triggered();
            }

        }
    }
    MouseArea {
        id: buttonMouseArea
        anchors.fill: parent
        onClicked: {
            animateDialogButton.start();
        }
    }
}