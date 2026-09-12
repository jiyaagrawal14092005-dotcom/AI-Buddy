import { useState } from "react";
import {
    Brain,
    Plus,
    Search,
    User,
    BookOpen,
    Lightbulb,
    Trash2,
    X,
} from "lucide-react";

function Memory() {
    const [memories, setMemories] = useState([
        {
            id: 1,
            title: "Project Preferences",
            text: "User prefers a clean futuristic interface with a dark blue theme.",
            category: "Preferences",
            icon: User,
        },
        {
            id: 2,
            title: "Learning",
            text: "Working on frontend development and AI projects.",
            category: "Learning",
            icon: BookOpen,
        },
        {
            id: 3,
            title: "Ideas",
            text: "Interested in building useful AI-powered productivity tools.",
            category: "Ideas",
            icon: Lightbulb,
        },
    ]);

    const [search, setSearch] = useState("");
    const [showForm, setShowForm] = useState(false);

    const [newTitle, setNewTitle] = useState("");
    const [newText, setNewText] = useState("");
    const [newCategory, setNewCategory] = useState("Personal");

    const addMemory = () => {
        if (!newTitle.trim() || !newText.trim()) {
            alert("Please enter a title and memory.");
            return;
        }

        const newMemory = {
            id: Date.now(),
            title: newTitle.trim(),
            text: newText.trim(),
            category: newCategory,
            icon: Brain,
        };

        setMemories((currentMemories) => [
            ...currentMemories,
            newMemory,
        ]);

        setNewTitle("");
        setNewText("");
        setNewCategory("Personal");
        setShowForm(false);
    };

    const deleteMemory = (id) => {
        setMemories((currentMemories) =>
            currentMemories.filter(
                (memory) => memory.id !== id
            )
        );
    };

    const closeForm = () => {
        setShowForm(false);
        setNewTitle("");
        setNewText("");
        setNewCategory("Personal");
    };

    const filteredMemories = memories.filter((memory) =>
        `${memory.title} ${memory.text} ${memory.category}`
            .toLowerCase()
            .includes(search.toLowerCase())
    );

    return (
        <div className="page-container">

            {/* HEADER */}
            <div className="page-header">

                <div>
                    <span className="page-eyebrow">
                        ZARVIS MEMORY
                    </span>

                    <h1>Memory</h1>

                    <p>
                        Things Zarvis remembers to better assist you.
                    </p>
                </div>

                <button
                    type="button"
                    className="primary-action"
                    onClick={() => setShowForm(true)}
                >
                    <Plus size={18} />
                    Add Memory
                </button>

            </div>


            {/* OVERVIEW */}
            <div className="memory-overview">

                <div className="glass-card memory-overview-card">

                    <div className="memory-big-icon">
                        <Brain size={23} />
                    </div>

                    <div>
                        <span>
                            Total Memories
                        </span>

                        <strong>
                            {memories.length}
                        </strong>
                    </div>

                </div>


                <div className="glass-card memory-overview-card">

                    <div className="memory-big-icon">
                        <User size={23} />
                    </div>

                    <div>
                        <span>
                            Personal
                        </span>

                        <strong>
                            {
                                memories.filter(
                                    (memory) =>
                                        memory.category === "Personal"
                                ).length
                            }
                        </strong>
                    </div>

                </div>


                <div className="glass-card memory-overview-card">

                    <div className="memory-big-icon">
                        <Lightbulb size={23} />
                    </div>

                    <div>
                        <span>
                            Ideas & Learning
                        </span>

                        <strong>
                            {
                                memories.filter(
                                    (memory) =>
                                        memory.category === "Ideas" ||
                                        memory.category === "Learning"
                                ).length
                            }
                        </strong>
                    </div>

                </div>

            </div>


            {/* ADD MEMORY FORM */}
            {showForm && (
                <section className="glass-card memory-form">

                    <div className="memory-form-header">

                        <div>
                            <h2>
                                Add New Memory
                            </h2>

                            <p>
                                Save something Zarvis should remember.
                            </p>
                        </div>

                        <button
                            type="button"
                            className="memory-form-close"
                            onClick={closeForm}
                        >
                            <X size={17} />
                        </button>

                    </div>


                    <div className="memory-form-grid">

                        <div className="memory-field">

                            <label>
                                Memory Title
                            </label>

                            <input
                                type="text"
                                placeholder="e.g. My Learning Goal"
                                value={newTitle}
                                onChange={(event) =>
                                    setNewTitle(event.target.value)
                                }
                            />

                        </div>


                        <div className="memory-field">

                            <label>
                                Category
                            </label>

                            <select
                                value={newCategory}
                                onChange={(event) =>
                                    setNewCategory(event.target.value)
                                }
                            >
                                <option value="Personal">
                                    Personal
                                </option>

                                <option value="Preferences">
                                    Preferences
                                </option>

                                <option value="Learning">
                                    Learning
                                </option>

                                <option value="Ideas">
                                    Ideas
                                </option>
                            </select>

                        </div>


                        <div className="memory-field memory-field-full">

                            <label>
                                Memory
                            </label>

                            <textarea
                                placeholder="What should Zarvis remember?"
                                value={newText}
                                onChange={(event) =>
                                    setNewText(event.target.value)
                                }
                            />

                        </div>

                    </div>


                    <div className="memory-form-actions">

                        <button
                            type="button"
                            className="memory-cancel"
                            onClick={closeForm}
                        >
                            Cancel
                        </button>

                        <button
                            type="button"
                            className="primary-action"
                            onClick={addMemory}
                        >
                            <Plus size={17} />
                            Save Memory
                        </button>

                    </div>

                </section>
            )}


            {/* SEARCH */}
            <div className="memory-search glass-card">

                <Search size={17} />

                <input
                    type="text"
                    placeholder="Search your memories..."
                    value={search}
                    onChange={(event) =>
                        setSearch(event.target.value)
                    }
                />

                {search && (
                    <button
                        type="button"
                        className="memory-search-clear"
                        onClick={() => setSearch("")}
                    >
                        <X size={15} />
                    </button>
                )}

            </div>


            {/* MEMORIES */}
            <section className="glass-card memory-page-card">

                <div className="card-header">

                    <div>
                        <h2>
                            Saved Memories
                        </h2>

                        <p>
                            Information Zarvis can use to personalize
                            your experience.
                        </p>
                    </div>

                    <span className="card-count">
                        {filteredMemories.length} Memories
                    </span>

                </div>


                <div className="memory-list">

                    {filteredMemories.length > 0 ? (
                        filteredMemories.map((memory) => {

                            const Icon = memory.icon;

                            return (
                                <div
                                    className="memory-item"
                                    key={memory.id}
                                >

                                    <div className="memory-item-icon">
                                        <Icon size={19} />
                                    </div>


                                    <div className="memory-item-info">

                                        <div className="memory-item-top">

                                            <strong>
                                                {memory.title}
                                            </strong>

                                            <span className="memory-category">
                                                {memory.category}
                                            </span>

                                        </div>

                                        <p>
                                            {memory.text}
                                        </p>

                                    </div>


                                    <button
                                        type="button"
                                        className="memory-delete"
                                        title="Delete memory"
                                        onClick={() =>
                                            deleteMemory(memory.id)
                                        }
                                    >
                                        <Trash2 size={17} />
                                    </button>

                                </div>
                            );
                        })
                    ) : (
                        <div className="memory-empty">

                            <Brain size={28} />

                            <strong>
                                No memories found
                            </strong>

                            <p>
                                Try a different search or add a new memory.
                            </p>

                        </div>
                    )}

                </div>

            </section>


            {/* INFO */}
            <div className="memory-info">

                <Brain size={17} />

                <span>
                    Memories are currently stored in frontend
                    state. They will be permanently saved when
                    Zarvis is connected to the backend.
                </span>

            </div>

        </div>
    );
}

export default Memory;