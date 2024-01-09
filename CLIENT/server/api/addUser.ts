import { PrismaClient } from '@prisma/client';
import { parse } from 'url'; // Node.js URL module

const prisma = new PrismaClient();

// Use Prisma's schema APIs to create the table
const createVideoSupabaseUserIdTable = async (tableName: string) => {  
    const formattedTableName = tableName.replace(/-/g, '_');
    try { 
        await prisma.$queryRawUnsafe(`
            CREATE TABLE IF NOT EXISTS ${formattedTableName} (
                video_id VARCHAR(255) PRIMARY KEY,
                video_title VARCHAR(255),
                video_description VARCHAR(255),
                video_directory VARCHAR(255)[],
                video_path VARCHAR(255),
                video_name VARCHAR(255),
                video_type VARCHAR(255),
                auto_generated_thumbnail_names VARCHAR(255)[],
                auto_generated_thumbnail_type VARCHAR(255),
                auto_generated_thumbnail_num INT,
                supabase_user_id VARCHAR(255) NOT NULL,
                FOREIGN KEY (supabase_user_id) REFERENCES profile(supabase_user_id)
            )`);
    } catch (error) {
        console.error('Error creating table:', error);
        throw new Error('Failed to create table');
    }
};

export default defineEventHandler(async (event) => {
    // Parse the URL and query string
    const parsedUrl = parse(event.req.url || '', true);
    const userId = parsedUrl.query.supabase_user_id;
  
    if (!userId) {
      return createError({ statusCode: 400, statusMessage: 'User ID is required.' });
    }
  
    try {
      const createdData = await prisma.profile.create({
        data: {
          supabase_user_id: userId,
        },
      });
  
      const tableName = "video_" + userId;
      await createVideoSupabaseUserIdTable(tableName);
  
      return createdData;
    } catch (error) {
      console.error('Error creating profile:', error);
      return createError({ statusCode: 500, statusMessage: 'Failed to create profile.' });
    } finally {
      await prisma.$disconnect();
    }  
});
