CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,                    -- Added to help with topic generation
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE topic_ideas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,                 -- Renamed from topic for clarity
    slug TEXT NOT NULL UNIQUE,           -- Added for URL-friendly titles
    description TEXT,                    -- Brief description/outline
    target_keywords TEXT,                -- JSON array of target keywords
    category_id INTEGER,
    status TEXT DEFAULT 'draft',         -- draft, approved, in_progress, published
    generation_prompt TEXT,              -- Store the successful generation prompt
    target_word_count INTEGER,           -- Desired article length
    priority INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL,           -- Made NOT NULL as articles must have topics
    title TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    content TEXT NOT NULL,
    content_version INTEGER DEFAULT 1,   -- Track content revisions
    category_id INTEGER,
    status TEXT DEFAULT 'draft',         -- draft, review, seo_optimization, published
    seo_score FLOAT,
    meta_description TEXT,
    keywords TEXT,                       -- JSON array of actual used keywords
    seo_feedback TEXT,                   -- Store SEO improvement suggestions
    review_feedback TEXT,                -- Store content review feedback
    published_at TIMESTAMP,              -- Removed DEFAULT for explicit publishing
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (topic_id) REFERENCES topic_ideas(id)
);

-- Indexes for common queries
CREATE INDEX idx_articles_category ON articles(category_id);
CREATE INDEX idx_articles_status ON articles(status);
CREATE INDEX idx_articles_topic ON articles(topic_id);

CREATE INDEX idx_topic_ideas_category ON topic_ideas(category_id);
CREATE INDEX idx_topic_ideas_status ON topic_ideas(status);
CREATE INDEX idx_topic_ideas_priority ON topic_ideas(priority); 