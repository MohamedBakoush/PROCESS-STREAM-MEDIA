import { PrismaClient } from '@prisma/client'; 
import { parse } from 'url'; // Node.js URL module

const prisma = new PrismaClient();

export default defineEventHandler(async (event) => {
  // Parse the URL and query string
const parsedUrl = parse(event.req.url || '', true);
const userId = parsedUrl.query.supabase_user_id;

if (!userId) {
    return createError({ statusCode: 400, statusMessage: 'User ID is required.' });
}

const userSpecificData = await prisma.info.findMany({
    where: {
        supabase_user_id: {
            in: [userId].flat()
        }
    }
});

  return userSpecificData;
});