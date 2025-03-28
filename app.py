import streamlit as st
import preprocessor as prp, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue() # here the data is binary stream format. i have to convert it into string. it get file from user using web screen
    data = bytes_data.decode("utf-8") # now it is converting into string
    # st.text(data)                # this will show the data in screen
    df = prp.preprocess(data)   # preprocessor class er preprocess function call korlam
    # st.dataframe(df) @ it will show df
    # fetch unique user
    uniq_user_list = df['user'].unique().tolist()
    uniq_user_list.remove('group_notification')
    uniq_user_list.sort()
    uniq_user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("Analyze for", uniq_user_list)

    if st.sidebar.button('Show Analysis'):
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)

        total_message, total_words ,total_media, numofLinks = helper.fetch_stats(selected_user, df)
        with col1:
            st.header( selected_user + "'s total Messages")
            st.title(total_message)
        with col2:
            st.header(selected_user + "'s total words")
            st.title(total_words)
        with col3:
            st.header(selected_user + "'s total media shared")
            st.title(total_media)
        with col4:
            st.header(selected_user + "'s total link shared")
            st.title(numofLinks)
        #monthly timeline
        st.title('Monthly Timeline')
        timeline = helper.timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    # daily timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.figure(figsize=(18, 10))
        ax.plot(daily_timeline['only_date'], daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # day activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        with col1:

            st.title('Most Busy Day')
            actvt = helper.weekly_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(actvt.index, actvt.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # month activity map
        with col2:
            st.title('Most Busy Month ')
            actvt = helper.monthly_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(actvt.index, actvt.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # fining the busiest users in group
        if selected_user == 'Overall':
            st.title('Most Active Persons')
            x , new_df= helper.most_busy_user(df)
            fig, ax = plt.subplots()
            col1 , col2 = st.columns(2)
            with col1:
                name = x.index
                count = x.values
                ax.bar(name, count, color = 'orange')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # wordCloud
        st.title("Word Cloud")
        wc_img = helper.create_wordCloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc_img)
        st.pyplot(fig)

        # emoji analysis
        emog_df = helper.emoji_finder(selected_user,df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emog_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emog_df[1], labels = emog_df[0])
            st.pyplot(fig)

        # show heatmap
        st.title('Weekly HeatMap')
        plt.figure(figsize=(20, 6))
        fig, ax = plt.subplots()
        ax = sns.heatmap(helper.user_heatmap(selected_user,df), cmap="coolwarm", annot=True, fmt=".0f")
        st.pyplot(fig)