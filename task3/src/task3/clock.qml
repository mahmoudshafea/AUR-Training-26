import QtQuick
import QtQuick.Shapes

Item {
    id: root

    width: 400
    height: 400

    required property var clockData

    Rectangle {
        id: clock

        anchors.centerIn: parent
        width: Math.min(parent.width, parent.height)
        height: width
        radius: width / 2

        color: "black"
        border.width: 8
        border.color: "#555555"

        Rectangle {
            id: hourHand

            width: 8
            height: clock.height * 0.25
            radius: width / 2
            color: "white"

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.verticalCenter

            transformOrigin: Item.Bottom

            rotation: (clockData.hours + clockData.mins / 60) * 30
        }

        Rectangle {
            id: minuteHand

            width: 5
            height: clock.height * 0.35
            radius: width / 2
            color: "white"

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.verticalCenter

            transformOrigin: Item.Bottom

            rotation: (clockData.mins + clockData.secs / 60) * 6
        }

        Rectangle {
            id: secondHand

            width: 2
            height: clock.height * 0.40
            radius: width / 2
            color: "red"

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.verticalCenter

            transformOrigin: Item.Bottom

            rotation: clockData.secs * 6
        }

        Rectangle {
            width: 14
            height: 14
            radius: width / 2
            color: "red"

            anchors.centerIn: parent
        }
    }
}