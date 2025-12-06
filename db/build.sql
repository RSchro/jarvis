CREATE TABLE IF NOT EXISTS application_paths (
    app_name text,
    app_path text
);

CREATE TABLE IF NOT EXISTS web_search_urls (
    url_name VARCHAR(50) UNIQUE,
    url_search VARCHAR(75)
);

CREATE TABLE IF NOT EXISTS user_preferences (
    prefs text
)