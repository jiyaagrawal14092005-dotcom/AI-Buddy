import { useEffect } from "react";
import { useBuddy } from "../context/BuddyContext";

function TestNotification() {
    const { addNotification } = useBuddy();

    useEffect(() => {
        const timer = setTimeout(() => {
            addNotification({
                title: "Download completed",
                message: "Python Cheatsheet_1.pdf has been downloaded successfully.",
                type: "success",
                icon: "download",
            });
        }, 2000);

        return () => {
            clearTimeout(timer);
        };
    }, [addNotification]);

    return null;
}

export default TestNotification;