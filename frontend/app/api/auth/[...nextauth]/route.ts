import NextAuth from "next-auth"
import DiscordProvider from "next-auth/providers/discord"

// this authOptions exported to use it in getServerSession functions 
// on server rendered pages
export const authOptions = { 
    providers: [
        DiscordProvider({
            clientId: process.env.DISCORD_CLIENT_ID,
            clientSecret: process.env.DISCORD_CLIENT_SECRET,
        }),
    ],
    pages: {
        signIn: '/signin'
    }
      
}

const handler = NextAuth(authOptions)

export { handler as GET, handler as POST}