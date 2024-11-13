import streamlit as st
def app():
    st.subheader("Create Document")
    # User upload zip file for document creation
    uploaded_doc_file = st.file_uploader("Upload a zip file with various code files for document creation", type="zip", key="doc_uploader")
    
    # Document summary generation
    if uploaded_doc_file and st.button("Generate Summary Document"):
        st.info("Generating summary...")
        with tempfile.NamedTemporaryFile(delete=False) as tmp_zip:
            tmp_zip.write(uploaded_doc_file.read())
            zip_file_path = tmp_zip.name

        combined_content = process_files_for_document(zip_file_path)

        if combined_content:
            # Generate summary using OpenAI
            summary_prompt = f"Summarize what code does and minimun words for summary are 2000 and use RAG implementation:\n\n{combined_content}"
            try:
                messages = [
                    {"role": "system", "content": "You are an AI that generates summaries."},
                    {"role": "user", "content": summary_prompt}
                ]
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages,
                    max_tokens=800,
                    temperature=0.7
                )
                summary = response.choices[0].message['content'].strip()
                
                # Create a Word document
                doc = Document()
                doc.add_heading('Combined Summary', level=1)
                doc.add_paragraph(summary)

                # Save document to a temporary file
                temp_doc_path = tempfile.mktemp(suffix='.docx')
                doc.save(temp_doc_path)

                # Provide download button
                with open(temp_doc_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Summary Document",
                        data=f,
                        file_name="summary_document.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                
                st.success("Summary generated! You can download the document.")

            except Exception as e:
                st.warning(f"Error generating summary: {e}")
        else:
            st.warning("No content found to summarize.")