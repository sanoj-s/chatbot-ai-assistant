# Display saved conversations in the sidebar
st.sidebar.header("Recent Conversations")
for idx, saved_conversation in enumerate(reversed(st.session_state.saved_conversations)):
    title = saved_conversation["title"]
    with st.sidebar.expander(f"{title}"):
        # Display the conversation messages
        for role, message in saved_conversation["conversation"]:
            st.markdown(f"**{role.capitalize()}**: {message}")

        # Add a "Save as Text" button for each conversation
        if st.button(f"Save '{title}' as Text", key=f"save_text_{idx}"):
            # Generate the conversation text
            conversation_text = "\n".join(
                [f"{role.capitalize()}: {message}" for role, message in saved_conversation["conversation"]]
            )

            # Write the conversation to a text file
            file_name = f"{title.replace(' ', '_')}.txt"
            with open(file_name, "w") as f:
                f.write(conversation_text)

            # Allow user to download the text file
            with open(file_name, "rb") as f:
                st.download_button(
                    label="Download Conversation",
                    data=f.read(),
                    file_name=file_name,
                    mime="text/plain",
                    key=f"download_text_{idx}",
                )
