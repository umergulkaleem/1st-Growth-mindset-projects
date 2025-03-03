import streamlit as st
import pandas as pd
import os
from io import BytesIO


# set up the app

st.set_page_config(page_title="Data Sweeper" ,page_icon="📁" ,layout='wide')
st.title("📁 Data Sweeper")
st.write("Transform your files between CSV and excel with data cleaning and data visualization!")


uploaded_files = st.file_uploader("Upload your files (CSV or Excel):",type=["csv","xlsx"],accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:  #loop after the file is uploaded
        file_ext=os.path.splitext(file.name)[-1].lower()   #to get the file type


        if file_ext ==".csv":
            df = pd.read_csv(file, header=0)
        elif file_ext ==".xlsx":
            df = pd.read_excel(file, header=0)
        else:
            st.error(f"Unsupported file type {file_ext}")
            continue

        #Display info about the file 

        st.write(f"**File Name:**{file.name}")
        st.write(f"**File Size:**{file.size/1024} KB")

        #show the 5 rpws of the data  in df

        st.write("preview the Head of the Dataframe")
        st.dataframe(df.head())
        
        #option for data cleaning

        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1,col2 = st.columns(2)

            with col1:
                if st.button(f"remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicate Removed Successfully")

            with col2:
                if st.button(f"Fill Missing Values For {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values Have been filled")
            
        # choose specific Cloumns to keep or convert 
        
        st.subheader("select Cloums to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}",df.columns,default=df.columns)
        df=df[columns]

        #Create new visualization 

        st.subheader("👀 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            numeric_df = df.select_dtypes(include=['number'])
            if numeric_df.shape[1] >= 2:
                st.bar_chart(numeric_df.iloc[:, :2])
            else:
                st.write("Not enough numeric columns for visualization")

        #Convert the File 
        st.subheader("🔃Conversion Options")
        conversion_type =st.radio(f"convert {file.name} to :",["CSV","Excel"],key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type =="CSV":
                df.to_csv(buffer,index=False)
                file_name = file.name.replace(file_ext,".csv")
                mime_type = "text/csv"

            elif conversion_type =="Excel":
                df.to_excel(buffer,index=False)
                file_name = file.name.replace(file_ext,".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            #download the file

            st.download_button(
                label=f"🔽 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
            st.success("🥳All Files Converted and Processed")