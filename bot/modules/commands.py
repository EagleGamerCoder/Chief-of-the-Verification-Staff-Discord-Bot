'''

info

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import discord
from discord import app_commands

# Modules

# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

async def setup(bot, context):
    # Catches command errors
    @bot.tree.error
    async def on_app_commmand_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        await context.log_error(interaction, "on_app_commmand_error", 1, error)

    # /setup_config
    @bot.tree.command(name="setup-config", description="Sets up the config for the Bot (Use `/setup_embeds` first).")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_config(interaction : discord.Interaction, role : discord.Role,  group_id : int, sub_group_id_one : int, sub_group_id_two : int, sub_group_id_three : int):
        await interaction.response.defer(ephemeral=True)

        await interaction.followup.send("Setting up config...", ephemeral=True)

        server_rules_ids = context.db.get_server_rules_ids(interaction.guild.id)
        if not server_rules_ids:
            await interaction.followup.send("Server rules ids, Invalid, Run `/setup_embeds` first.", ephemeral=True)
            return

        try:
            context.db.set_guild_config(interaction.guild.id, interaction.channel.id, role.id, group_id, sub_group_id_one, sub_group_id_two, sub_group_id_three)

            await interaction.followup.send(
                "✅ Setup complete.", 
                ephemeral=True,
            )
        except Exception as e:
            await context.log_error(interaction, "setup_config", 1, e)
    
    # /setup_embeds
    @bot.tree.command(name="setup-embeds", description="Sets up the Server rules embed and the verification emded (Use in #Verification).")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_embeds(interaction : discord.Interaction, server_rules_channel_id : str, server_rules_message_id : str | None):
        await interaction.response.defer(ephemeral=True)

        await interaction.followup.send("Setting up embeds...", ephemeral=True)

        # Validate channel
        try:
            server_rules_channel = interaction.guild.get_channel(int(server_rules_channel_id))
            if server_rules_channel is None:
                await interaction.followup.send("❌ Invalid channel ID.", ephemeral=True)
                return
        except:
            await interaction.followup.send("❌ Invalid channel ID format.", ephemeral=True)
            return

        try:
            
            msg = None

            if server_rules_message_id == None:
                # The embeds do not exist and need to be created
                
                # Send rules embed
                await server_rules_channel.send("# __**Server Rules:**__")
                msg = await server_rules_channel.send(embed=context.create_server_rules_embed())
                await msg.add_reaction('✅')

                # Send verification embed
                await interaction.channel.send(f"# __**Welcome to the {interaction.guild.name} Discord Server!**__")
                await interaction.channel.send(embed=context.create_verification_embed(),view=context.VerifyView())

                # Final response
                await interaction.followup.send("✅ Setup complete.", ephemeral=True)
            else:
                # The embeds do exist and the info from them only needs to be saved

                # validate server_rules_message_id
                try:
                    msg = await server_rules_channel.fetch_message(int(server_rules_message_id))
                except discord.NotFound:
                    await interaction.followup.send("❌ Invalid message ID.")
                    return
                except discord.Forbidden:
                    await context.log_error(interaction, "setup_embeds", 1, "Missing Read Message History permission")
                    return
                except Exception as e:
                    await context.log_error(interaction, "setup_embeds", 2, e)
                    return

            if msg == None:
                return

            context.db.save_server_rules_ids(interaction.guild.id, server_rules_channel.id, msg.id)

        except Exception as e:
            await context.log_error(interaction, "setup_embeds", 3, e)
            return