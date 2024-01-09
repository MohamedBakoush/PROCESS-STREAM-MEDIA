import { PrismaClient } from '@prisma/client';
import { parse } from 'url';

const prisma = new PrismaClient();

export default defineEventHandler(async (event) => {
  try {
    // Parse the URL and query string
    const parsedUrl = parse(event.req.url || '', true);
    const userId = parsedUrl.query.supabase_user_id;

    if (!userId) {
      return createError({ statusCode: 400, statusMessage: 'User ID is required.' });
    }

    const tableName = `video_${userId}`;
    const formattedTableName = tableName.replace(/-/g, '_');
    
    const userSpecificData = await prisma.$queryRawUnsafe(`
      SELECT 
        video_id,
        video_title,
        video_description,
        auto_generated_thumbnail_num
      FROM "${formattedTableName}"
      WHERE supabase_user_id = '${userId}'
    `);

    return userSpecificData;
  } catch (error) {
    console.error('Error in Prisma handler:', error);
    return createError({ statusCode: 500, statusMessage: 'Internal Server Error. Please contact support for assistance.' });
  } finally {
    await prisma.$disconnect();
  }
});