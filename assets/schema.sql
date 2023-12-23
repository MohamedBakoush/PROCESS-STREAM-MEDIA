-- Create a table to store video information
CREATE TABLE info (
    info_id VARCHAR(255) PRIMARY KEY, 
    supabase_user_id VARCHAR(255) NOT NULL,
    public BOOLEAN NOT NULL DEFAULT TRUE,
    video_name VARCHAR(255),
    video_description VARCHAR(255)
);

-- Create a table to store video files
CREATE TABLE videos (
    video_id VARCHAR(255) PRIMARY KEY,
    info_id VARCHAR(255),
    file_dir VARCHAR(255)[],
    file_path VARCHAR(255),
    file_name VARCHAR(255),
    file_type VARCHAR(255),
    FOREIGN KEY (info_id) REFERENCES info(info_id)
);

-- Create a table to store thumbnail information
CREATE TABLE thumbnails (
    thumbnail_id SERIAL PRIMARY KEY,
    video_id VARCHAR(255),
    thumb_num INT,  
    file_dir VARCHAR(255)[],
    file_path VARCHAR(255),
    file_name VARCHAR(255),
    file_type VARCHAR(255),
    FOREIGN KEY (video_id) REFERENCES videos(video_id)
);