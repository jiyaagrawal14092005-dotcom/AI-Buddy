import robotImage from "../images/zarvis_robot_transparent.png";
import "../styles/cosmos.css";

function ChatBox() {
    return (
        <div className="zarvis-robot-area">

            <div className="robot-cosmos">

                <div className="cosmic-nebula nebula-purple"></div>

                <div className="cosmic-nebula nebula-blue"></div>

                <div className="cosmic-nebula nebula-center"></div>


                {/* Cosmic Stars */}

                <span className="cosmic-star star-1">
                    ✦
                </span>

                <span className="cosmic-star star-2">
                    ✦
                </span>

                <span className="cosmic-star star-3">
                    ✦
                </span>

                <span className="cosmic-star star-4">
                    ✦
                </span>

                <span className="cosmic-star star-5">
                    ✦
                </span>

                <span className="cosmic-star star-6">
                    ✦
                </span>

                <span className="cosmic-star star-7">
                    ✦
                </span>

                <span className="cosmic-star star-8">
                    ✦
                </span>


                {/* Tiny Stars */}

                <span className="tiny-star tiny-1"></span>

                <span className="tiny-star tiny-2"></span>

                <span className="tiny-star tiny-3"></span>

                <span className="tiny-star tiny-4"></span>

                <span className="tiny-star tiny-5"></span>

                <span className="tiny-star tiny-6"></span>

                <span className="tiny-star tiny-7"></span>

                <span className="tiny-star tiny-8"></span>

                <span className="tiny-star tiny-9"></span>

                <span className="tiny-star tiny-10"></span>


                {/* Galaxy Streak */}

                <div className="galaxy-streak"></div>

            </div>


            {/* =================================================
                ROBOT
            ================================================= */}

            <div className="robot-visual">


                {/* Orbit Rings */}

                <div className="robot-orbit orbit-1"></div>

                <div className="robot-orbit orbit-2"></div>

                <div className="robot-orbit orbit-3"></div>


                {/* Orbit Glow */}

                <div className="orbit-glow glow-1"></div>

                <div className="orbit-glow glow-2"></div>


                {/* Robot Image */}

                <div className="robot-image-wrap">

                    <img
                        src={robotImage}
                        alt="Zarvis AI Assistant"
                        className="zarvis-robot-image"
                    />

                </div>


                {/* =================================================
                    SPEECH BUBBLE
                ================================================= */}

                <div className="robot-speech-bubble">

                    <strong>
                        Hi! I'm Zarvis 👋
                    </strong>

                    <span>
                        Your smart AI assistant.
                    </span>

                    <span>
                        How can I help you today?
                    </span>

                    <div className="speech-arrow"></div>

                </div>


                {/* =================================================
                    ROBOT PLATFORM
                ================================================= */}

                <div className="robot-platform">

                    <div className="platform-ring ring-1"></div>

                    <div className="platform-ring ring-2"></div>

                    <div className="platform-ring ring-3"></div>

                    <div className="platform-core"></div>

                </div>

            </div>

        </div>
    );
}

export default ChatBox;