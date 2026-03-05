-- ArtFunder Database Schema
-- PostgreSQL schema for art-backed investment platform

CREATE SCHEMA IF NOT EXISTS artfunder;

-- Enum types
DO $$ BEGIN
    CREATE TYPE artfunder.user_role AS ENUM ('investor', 'artist', 'admin');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE artfunder.art_category AS ENUM ('painting', 'sculpture', 'photography', 'print', 'mixed_media');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE artfunder.artwork_status AS ENUM ('draft', 'active', 'funded', 'completed', 'defaulted');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE artfunder.funding_status AS ENUM ('open', 'funded', 'closed', 'repaying');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE artfunder.risk_level AS ENUM ('A', 'B', 'C', 'D');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE artfunder.investment_status AS ENUM ('pending', 'confirmed', 'completed', 'cancelled');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE artfunder.payment_status AS ENUM ('pending', 'completed', 'failed');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE artfunder.listing_status AS ENUM ('listed', 'sold', 'withdrawn');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE artfunder.update_type AS ENUM ('status_update', 'valuation_update', 'financial_update', 'milestone');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE artfunder.notification_type AS ENUM ('general', 'investment', 'repayment', 'project_update');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Users
CREATE TABLE IF NOT EXISTS artfunder.users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL DEFAULT '',
    last_name VARCHAR(100) NOT NULL DEFAULT '',
    role artfunder.user_role NOT NULL DEFAULT 'investor',
    phone VARCHAR(50),
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_users_email ON artfunder.users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON artfunder.users(role);

-- Galleries
CREATE TABLE IF NOT EXISTS artfunder.galleries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    registration_number VARCHAR(100) UNIQUE,
    address TEXT,
    user_id INTEGER REFERENCES artfunder.users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Artworks
CREATE TABLE IF NOT EXISTS artfunder.artworks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category artfunder.art_category NOT NULL,
    status artfunder.artwork_status DEFAULT 'draft',
    artist_name VARCHAR(255),
    medium VARCHAR(500),
    origin_country VARCHAR(100),
    year_created VARCHAR(20),
    dimensions VARCHAR(200),
    estimated_value NUMERIC(14,2),
    acquisition_cost NUMERIC(14,2),
    appreciation_rate NUMERIC(5,2),
    artist_id INTEGER REFERENCES artfunder.users(id),
    image_url VARCHAR(500),
    provenance TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_artworks_status ON artfunder.artworks(status);
CREATE INDEX IF NOT EXISTS idx_artworks_category ON artfunder.artworks(category);
CREATE INDEX IF NOT EXISTS idx_artworks_artist ON artfunder.artworks(artist_id);

-- Investment Opportunities (funding campaigns for artworks)
CREATE TABLE IF NOT EXISTS artfunder.investment_opportunities (
    id SERIAL PRIMARY KEY,
    artwork_id INTEGER NOT NULL REFERENCES artfunder.artworks(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    funding_goal NUMERIC(14,2) NOT NULL,
    amount_raised NUMERIC(14,2) DEFAULT 0,
    minimum_investment NUMERIC(10,2) DEFAULT 100,
    interest_rate NUMERIC(5,2) NOT NULL,
    term_months INTEGER NOT NULL,
    start_date DATE,
    end_date DATE,
    funding_status artfunder.funding_status DEFAULT 'open',
    risk_level artfunder.risk_level DEFAULT 'B',
    funding_type VARCHAR(50) DEFAULT 'fractional_ownership',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_opportunities_status ON artfunder.investment_opportunities(funding_status);
CREATE INDEX IF NOT EXISTS idx_opportunities_artwork ON artfunder.investment_opportunities(artwork_id);

-- Investments
CREATE TABLE IF NOT EXISTS artfunder.investments (
    id SERIAL PRIMARY KEY,
    opportunity_id INTEGER NOT NULL REFERENCES artfunder.investment_opportunities(id),
    investor_id INTEGER NOT NULL REFERENCES artfunder.users(id),
    amount NUMERIC(14,2) NOT NULL,
    ownership_percentage NUMERIC(5,2),
    expected_return NUMERIC(14,2),
    status artfunder.investment_status DEFAULT 'pending',
    invested_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(opportunity_id, investor_id)
);
CREATE INDEX IF NOT EXISTS idx_investments_investor ON artfunder.investments(investor_id);
CREATE INDEX IF NOT EXISTS idx_investments_opportunity ON artfunder.investments(opportunity_id);

-- Project Updates
CREATE TABLE IF NOT EXISTS artfunder.project_updates (
    id SERIAL PRIMARY KEY,
    artwork_id INTEGER NOT NULL REFERENCES artfunder.artworks(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    update_type artfunder.update_type DEFAULT 'status_update',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Notifications
CREATE TABLE IF NOT EXISTS artfunder.notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES artfunder.users(id),
    title VARCHAR(255) NOT NULL,
    message TEXT,
    notification_type artfunder.notification_type DEFAULT 'general',
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON artfunder.notifications(user_id);

-- Follow Artworks
CREATE TABLE IF NOT EXISTS artfunder.follow_artworks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES artfunder.users(id),
    artwork_id INTEGER NOT NULL REFERENCES artfunder.artworks(id),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, artwork_id)
);

-- FAQs
CREATE TABLE IF NOT EXISTS artfunder.faqs (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

-- Repayments
CREATE TABLE IF NOT EXISTS artfunder.repayments (
    id SERIAL PRIMARY KEY,
    opportunity_id INTEGER NOT NULL REFERENCES artfunder.investment_opportunities(id),
    amount NUMERIC(14,2) NOT NULL,
    repayment_date DATE NOT NULL,
    is_principal BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Dividends
CREATE TABLE IF NOT EXISTS artfunder.dividends (
    id SERIAL PRIMARY KEY,
    investor_id INTEGER NOT NULL REFERENCES artfunder.users(id),
    opportunity_id INTEGER NOT NULL REFERENCES artfunder.investment_opportunities(id),
    amount NUMERIC(14,2) NOT NULL,
    is_paid BOOLEAN DEFAULT FALSE,
    paid_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Investor Votings
CREATE TABLE IF NOT EXISTS artfunder.investor_votings (
    id SERIAL PRIMARY KEY,
    opportunity_id INTEGER NOT NULL REFERENCES artfunder.investment_opportunities(id),
    question TEXT NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- User Votes
CREATE TABLE IF NOT EXISTS artfunder.user_votes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES artfunder.users(id),
    voting_id INTEGER NOT NULL REFERENCES artfunder.investor_votings(id),
    vote_choice VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, voting_id)
);

-- Payments
CREATE TABLE IF NOT EXISTS artfunder.payments (
    id SERIAL PRIMARY KEY,
    investor_id INTEGER NOT NULL REFERENCES artfunder.users(id),
    investment_id INTEGER NOT NULL REFERENCES artfunder.investments(id),
    amount NUMERIC(14,2) NOT NULL,
    payment_status artfunder.payment_status DEFAULT 'pending',
    transaction_id VARCHAR(100) UNIQUE,
    reference_number VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Secondary Market
CREATE TABLE IF NOT EXISTS artfunder.secondary_market (
    id SERIAL PRIMARY KEY,
    investment_id INTEGER NOT NULL REFERENCES artfunder.investments(id),
    seller_id INTEGER NOT NULL REFERENCES artfunder.users(id),
    listing_price NUMERIC(14,2) NOT NULL,
    status artfunder.listing_status DEFAULT 'listed',
    listed_at TIMESTAMP DEFAULT NOW(),
    sold_at TIMESTAMP
);

-- Auto Invest Settings
CREATE TABLE IF NOT EXISTS artfunder.auto_invest (
    id SERIAL PRIMARY KEY,
    investor_id INTEGER NOT NULL REFERENCES artfunder.users(id),
    max_investment_amount NUMERIC(14,2) NOT NULL,
    min_interest_rate NUMERIC(5,2),
    max_appreciation_rate NUMERIC(5,2),
    preferred_risk_levels VARCHAR(20),
    preferred_categories VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Seed admin user (password: admin123 - change in production)
-- Password hash is sha256 of 'admin123'
INSERT INTO artfunder.users (email, password_hash, first_name, last_name, role, is_verified, is_active, is_staff)
VALUES ('admin@artfunder.com', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Admin', 'User', 'admin', true, true, true)
ON CONFLICT (email) DO NOTHING;
