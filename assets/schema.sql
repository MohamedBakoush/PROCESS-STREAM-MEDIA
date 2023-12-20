-- Create a table to store video information
CREATE TABLE videos (
    video_id VARCHAR(255) PRIMARY KEY,  
    file_dir VARCHAR(255)[],
    file_path VARCHAR(255),
    file_name VARCHAR(255),
    file_type VARCHAR(255)
);

-- Create a table to store video information
CREATE TABLE info (
    info_id SERIAL PRIMARY KEY, 
    video_id VARCHAR(255),
    video_title VARCHAR(255),
    video_description VARCHAR(255), 
    FOREIGN KEY (video_id) REFERENCES videos(video_id)
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

-- Create a table to store download status
CREATE TABLE download_status ( 
    video_id VARCHAR(255) PRIMARY KEY,
    video_download_status VARCHAR(255),
    thumbnail_download_status VARCHAR(255)
);