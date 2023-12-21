import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

export default defineEventHandler(async (event) => {
    try { 
        // Fetch data from the 'info' table using Prisma
        const allInfo = await prisma.info.findMany();
        return allInfo;
    } catch (error) {
        console.error(error);
        return createError({ statusCode: 500, message: 'Internal Server Error' });
    }
});