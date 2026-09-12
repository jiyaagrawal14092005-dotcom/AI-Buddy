import {
    Mic,
    Sparkles,
} from "lucide-react";

function ChatBox() {
    return (
        <div className="zarvis-robot-area">

            {/* Galaxy glow */}
            <div className="galaxy-glow galaxy-glow-one"></div>
            <div className="galaxy-glow galaxy-glow-two"></div>
            <div className="galaxy-glow galaxy-glow-three"></div>

            {/* Stars */}
            <div className="galaxy-stars stars-one"></div>
            <div className="galaxy-stars stars-two"></div>

            <span className="space-star star-one">✦</span>
            <span className="space-star star-two">✦</span>
            <span className="space-star star-three">✧</span>
            <span className="space-star star-four">✦</span>
            <span className="space-star star-five">·</span>

            {/* Robot glow */}
            <div className="robot-glow"></div>

            {/* Orbit rings */}
            <div className="robot-orbit robot-orbit-1">
                <span className="orbit-particle"></span>
            </div>

            <div className="robot-orbit robot-orbit-2">
                <span className="orbit-particle"></span>
            </div>

            <div className="robot-orbit robot-orbit-3">
                <span className="orbit-particle"></span>
            </div>

            {/* Robot */}
            <div className="cute-zarvis">

                {/* Left ear */}
                <div className="zarvis-ear zarvis-ear-left">
                    <div className="ear-inner"></div>
                </div>

                {/* Right ear */}
                <div className="zarvis-ear zarvis-ear-right">
                    <div className="ear-inner"></div>
                </div>

                {/* Head */}
                <div className="zarvis-head">

                    <div className="zarvis-face">

                        <div className="zarvis-eye">
                            <span></span>
                        </div>

                        <div className="zarvis-eye">
                            <span></span>
                        </div>

                        <div className="zarvis-smile"></div>

                    </div>

                    <div className="zarvis-head-shine"></div>

                </div>

                {/* Neck */}
                <div className="zarvis-neck"></div>

                {/* Body */}
                <div className="zarvis-body">

                    <div className="zarvis-chest">
                        Z
                    </div>

                    <div className="zarvis-body-shine"></div>

                </div>

                {/* Arms */}
                <div className="zarvis-arm zarvis-arm-left">
                    <div className="zarvis-hand"></div>
                </div>

                <div className="zarvis-arm zarvis-arm-right">
                    <div className="zarvis-hand"></div>
                </div>

            </div>

            {/* Platform */}
            <div className="zarvis-platform">

                <div className="platform-light"></div>

                <div className="platform-ring"></div>

                <div className="platform-core"></div>

            </div>

            {/* Speech bubble */}
            <div className="robot-message">

                <strong>
                    I'm here for you!
                </strong>

                <span>
                    Plan&nbsp; · &nbsp;Organize&nbsp; · &nbsp;Achieve
                </span>

            </div>

            {/* Small voice indicator */}
            <div className="robot-voice">

                <Mic size={13} />

                <span>Ready</span>

            </div>

        </div>
    );
}

export default ChatBox;