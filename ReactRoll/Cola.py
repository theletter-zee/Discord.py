

class saveRoles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    async def roleaccount(self, msgID):
        rolenames = await self.read_roles()

        with open('roles.json','r') as f:
            rolenames = json.load(f)

        if str(msgID) in rolenames:
            return False
        else:
                
            rolenames[str(msgID)] = {}
            rolenames[str(msgID)]['roles'] = []


            with open('roles.json', 'w') as f:
                json.dump(rolenames, f, indent=2)
            return True



    async def read_roles(self):
        with open('roles.json', 'r') as f:
            rolenames = json.load(f)
        return rolenames
    




class mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        # -  -  - Create Role -  -  - #

        with open('roles.json','r') as f:
            role_id = json.load(f)

        for i in role_id:
            msg_id = i

        rolenames = await saveRoles(str(msg_id)).read_roles()

        for i in rolenames[str(msg_id)]['roles']:
            if i['emoji'] == payload.emoji.name and i['message_id'] == payload.message_id:
                role = discord.utils.get(self.bot.get_guild(payload.guild_id).roles, id=i['role_id'])

                await payload.member.add_roles(role)
        
        # -  -  - Message Cache Role -  -  - #

        if "\ud83c\udfa5" == payload.emoji.name and payload.id == 828696941281148950:
            print("This works.")


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # -  -  - Create Role -  -  - #

        with open('roles.json','r') as f:
            role_id = json.load(f)

        for i in role_id:
            msg_id = i

        rolenames = await saveRoles(str(msg_id)).read_roles()

        for i in rolenames[str(msg_id)]['roles']:
            if i['emoji'] == payload.emoji.name and i['message_id'] == payload.message_id:
                role = discord.utils.get(self.bot.get_guild(payload.guild_id).roles, id=i['role_id'])

                await self.bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
        




    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, emoji=None, role: discord.Role = None):
        if emoji is not None and role is not None:

            msg = await ctx.channel.send(content='Loading...') #Place holder so I can get the id 
            await saveRoles(msg.id).roleaccount(msg.id)
            rolenames = await saveRoles(msg.id).read_roles()


            
            role_attrs = {
                'role_name': role.name,
                'role_id': role.id,
                'emoji': emoji,
                'message_id': msg.id
            }

            rolenames[str(msg.id)]['roles'].append(role_attrs)
            

            role_name = rolenames[str(msg.id)]['roles'][0]['role_name']
            emj = rolenames[str(msg.id)]['roles'][0]['emoji']



            role_embed = discord.Embed(title='React for Roles',color=discord.Color.blurple())
            role_embed.add_field(name=f'{emj}  {role_name}', value='\u200b',inline=False)

            #Edit the id of the msg
            role_embed.set_footer(text='Id: '+str(msg.id))
            await msg.edit(content='', embed=role_embed) 

            await msg.add_reaction(emoji)

            with open('roles.json','w') as f:
                json.dump(rolenames, f, indent=2)


        else:
           await ctx.send('**Example**: .createrole (emoji) (@rolename)')
           await ctx.send(file=discord.File('roleExample.png'))
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, emoji=None, role: discord.Role = None, msgID: discord.Message = None):
        try:
            if emoji is not None and role is not None and msgID is not None :
                await saveRoles(msgID.id).roleaccount(msgID.id)
                rolenames = await saveRoles(msgID.id).read_roles()


                role_attrs = {
                    'role_name': role.name,
                    'role_id': role.id,
                    'emoji': emoji,
                    'message_id': msgID.id
                }

                rolenames[str(msgID.id)]['roles'].append(role_attrs)            


                role_embed = discord.Embed(title='React for Roles',color=discord.Color.blurple())

                for role in rolenames[str(msgID.id)]['roles']:
                    roleName = role['role_name']
                    role_emoji = role['emoji'] 

                    role_embed.add_field(name=f'{role_emoji}  {roleName}', value=f'\u200b',inline=False)

                #Edit the id of the msg
                role_embed.set_footer(text='Id: '+str(msgID.id))
                await msgID.edit(embed=role_embed)

                await msgID.add_reaction(emoji)

                with open('roles.json', 'w') as f:
                    json.dump(rolenames, f, indent=2)
            else:
                await ctx.send('**Example**: .addrole (emoji) (@rolename)')
                await ctx.send(file=discord.File('addroleExample.png'))
        except discord.Forbidden:
            await ctx.channel.send('Cannot edit msg by another user')




def setup(bot):
    bot.add_cog(saveRoles(bot))
    bot.add_cog(mod(bot))
