import { useState } from "react";
import { useLocation } from "react-router-dom";

import {
    Plus,
    Search,
    Brain,
    Trash2,
    Clock3,
} from "lucide-react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";


const initialMemories = [
    {
        id: 1,
        title: "Project Name",
        description:
            "The current AI buddy project is called Zarvis.",
        category: "PROJECT",
    },
    {
        id: 2,
        title: "Study Preference",
        description:
            "Prefer simple explanations with practical examples.",
        category: "PREFERENCE",
    },
    {
        id: 3,
        title: "Productivity Style",
        description:
            "Keep tasks organized and easy to follow.",
        category: "PRODUCTIVITY",
    },
    {
        id: 4,
        title: "Interface Preference",
        description:
            "Prefer a clean, modern and futuristic interface.",
        category: "PERSONAL",
    },
];


function Memory() {

    const location = useLocation();


    const [memories, setMemories] =
        useState(initialMemories);


    const [search, setSearch] =
        useState("");


    /*
     * Dashboard → Save Memory
     * Automatically opens the memory creator.
     */
    const [showForm, setShowForm] =
        useState(
            location.state?.openForm === true
        );


    const [newMemory, setNewMemory] =
        useState({
            title: "",
            description: "",
            category: "PERSONAL",
        });


    const filteredMemories =
        memories.filter(
            (memory) =>
                `${memory.title} ${memory.description} ${memory.category}`
                    .toLowerCase()
                    .includes(
                        search.toLowerCase()
                    )
        );


    const projectCount =
        memories.filter(
            (memory) =>
                memory.category === "PROJECT"
        ).length;


    const preferenceCount =
        memories.filter(
            (memory) =>
                memory.category === "PREFERENCE"
        ).length;


    const deleteMemory = (id) => {

        setMemories((current) =>
            current.filter(
                (memory) =>
                    memory.id !== id
            )
        );

    };


    const handleAddMemory = (e) => {

        e.preventDefault();


        if (
            !newMemory.title.trim() ||
            !newMemory.description.trim()
        ) {
            return;
        }


        const memory = {

            id: Date.now(),

            title:
                newMemory.title.trim(),

            description:
                newMemory.description.trim(),

            category:
                newMemory.category,

        };


        setMemories((current) => [
            memory,
            ...current,
        ]);


        setNewMemory({
            title: "",
            description: "",
            category: "PERSONAL",
        });


        setShowForm(false);

    };


    return (

        <div className="app">

            <Sidebar />


            <main className="main-content">

                <Navbar />


                <div className="memory-page-final">


                    {/* ================= HEADER ================= */}

                    <div className="memory-header-final">

                        <div className="memory-header-left-final">

                            <div className="memory-eyebrow-final">

                                <Brain size={14} />

                                <span>
                                    ZARVIS MEMORY SYSTEM
                                </span>

                            </div>


                            <h1>
                                Memory
                            </h1>


                            <p>
                                Important information Zarvis remembers
                                to make your experience more personal.
                            </p>

                        </div>


                        <button
                            type="button"
                            className="memory-add-final"
                            onClick={() =>
                                setShowForm(
                                    !showForm
                                )
                            }
                        >

                            <Plus size={18} />

                            <span>
                                Add Memory
                            </span>

                        </button>

                    </div>


                    {/* ================= STATS ================= */}

                    <div className="memory-stats-final">


                        <div className="memory-stat-final">

                            <span>
                                TOTAL MEMORIES
                            </span>

                            <strong>
                                {memories.length}
                            </strong>

                        </div>


                        <div className="memory-stat-final">

                            <span>
                                PROJECT
                            </span>

                            <strong>
                                {projectCount}
                            </strong>

                        </div>


                        <div className="memory-stat-final">

                            <span>
                                PREFERENCES
                            </span>

                            <strong>
                                {preferenceCount}
                            </strong>

                        </div>


                        <div className="memory-stat-final">

                            <span>
                                MEMORY STATUS
                            </span>

                            <strong className="memory-status-final">
                                ACTIVE
                            </strong>

                        </div>

                    </div>


                    {/* ================= CREATE MEMORY ================= */}

                    {showForm && (

                        <form
                            className="memory-create-final"
                            onSubmit={
                                handleAddMemory
                            }
                        >


                            <div className="memory-create-top-final">

                                <div>

                                    <span>
                                        MEMORY CREATOR
                                    </span>

                                    <h2>
                                        Save New Memory
                                    </h2>

                                </div>


                                <button
                                    type="button"
                                    className="memory-close-final"
                                    onClick={() =>
                                        setShowForm(false)
                                    }
                                    aria-label="Close memory form"
                                >
                                    ×
                                </button>

                            </div>


                            <div className="memory-form-final">


                                <div className="memory-input-final">

                                    <label>
                                        Memory Title
                                    </label>

                                    <input
                                        type="text"
                                        placeholder="e.g. Favorite study style"
                                        value={
                                            newMemory.title
                                        }
                                        onChange={(e) =>
                                            setNewMemory({
                                                ...newMemory,
                                                title:
                                                    e.target.value,
                                            })
                                        }
                                    />

                                </div>


                                <div className="memory-input-final">

                                    <label>
                                        Category
                                    </label>

                                    <select
                                        value={
                                            newMemory.category
                                        }
                                        onChange={(e) =>
                                            setNewMemory({
                                                ...newMemory,
                                                category:
                                                    e.target.value,
                                            })
                                        }
                                    >

                                        <option value="PERSONAL">
                                            PERSONAL
                                        </option>

                                        <option value="PROJECT">
                                            PROJECT
                                        </option>

                                        <option value="PREFERENCE">
                                            PREFERENCE
                                        </option>

                                        <option value="PRODUCTIVITY">
                                            PRODUCTIVITY
                                        </option>

                                    </select>

                                </div>


                                <div className="memory-input-final memory-input-full-final">

                                    <label>
                                        Memory
                                    </label>

                                    <textarea
                                        placeholder="What should Zarvis remember?"
                                        value={
                                            newMemory.description
                                        }
                                        onChange={(e) =>
                                            setNewMemory({
                                                ...newMemory,
                                                description:
                                                    e.target.value,
                                            })
                                        }
                                    />

                                </div>

                            </div>


                            <button
                                type="submit"
                                className="memory-save-final"
                            >

                                <Plus size={16} />

                                SAVE MEMORY

                            </button>

                        </form>

                    )}


                    {/* ================= SEARCH ================= */}

                    <div className="memory-search-row-final">


                        <div className="memory-search-final">

                            <Search size={18} />

                            <input
                                type="text"
                                placeholder="Search memories..."
                                value={search}
                                onChange={(e) =>
                                    setSearch(
                                        e.target.value
                                    )
                                }
                            />

                        </div>


                        <div className="memory-found-final">

                            <span></span>

                            {filteredMemories.length}
                            {" "}
                            MEMORIES FOUND

                        </div>

                    </div>


                    {/* ================= SAVED MEMORIES ================= */}

                    <section className="memory-list-final">


                        <div className="memory-list-header-final">


                            <div>

                                <span>
                                    KNOWLEDGE STORE // 04
                                </span>

                                <h2>
                                    Saved Memories
                                </h2>

                            </div>


                            <div className="memory-core-final">

                                <Brain size={15} />

                                <span>
                                    CORE ACTIVE
                                </span>

                            </div>

                        </div>


                        <div className="memory-items-final">


                            {filteredMemories.length === 0 ? (

                                <div className="memory-empty-final">

                                    <Brain size={32} />

                                    <h3>
                                        No memories found
                                    </h3>

                                    <p>
                                        Try another search or add
                                        a new memory.
                                    </p>

                                </div>

                            ) : (

                                filteredMemories.map(
                                    (memory) => (

                                        <div
                                            className="memory-item-final"
                                            key={memory.id}
                                        >


                                            <div className="memory-item-icon-final">

                                                <Brain size={19} />

                                            </div>


                                            <div className="memory-item-content-final">


                                                <div className="memory-item-title-final">

                                                    <h3>
                                                        {memory.title}
                                                    </h3>

                                                    <span>
                                                        {memory.category}
                                                    </span>

                                                </div>


                                                <p>
                                                    {memory.description}
                                                </p>


                                                <div className="memory-item-meta-final">

                                                    <span>

                                                        <Clock3 size={12} />

                                                        Today

                                                    </span>


                                                    <span>

                                                        <Brain size={12} />

                                                        Zarvis Memory

                                                    </span>

                                                </div>

                                            </div>


                                            <button
                                                type="button"
                                                className="memory-delete-final"
                                                onClick={() =>
                                                    deleteMemory(
                                                        memory.id
                                                    )
                                                }
                                                title="Delete memory"
                                                aria-label="Delete memory"
                                            >

                                                <Trash2 size={16} />

                                            </button>

                                        </div>

                                    )
                                )

                            )}

                        </div>

                    </section>


                </div>

            </main>

        </div>

    );

}


export default Memory;