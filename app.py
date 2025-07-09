import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file") # streamlit documentation
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # this file actually a stream we have to convert in string
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # from here we create a dropdown from where we can select any user and dropdown have those usernames who are involved in a group
    # fetch unique users

    user_list = df['user'].unique().tolist()
    # user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"overall")

    selected_user = st.sidebar.selectbox("show Analysis with respect to",user_list)
    if st.sidebar.button("Show Analysis"):

        num_messages,words,num_media_message, num_links = helper.fetch_stats(selected_user,df)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_message)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation = 'vertical')
        st.title("Monthly Timeline")
        st.pyplot(fig)

        # daily timeline
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='orange')
        plt.xticks(rotation = 'vertical')
        st.title("Daily Timeline")
        st.pyplot(fig)

        # Activity map
        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = "darkcyan")
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        #heatmap
        st.title("Weekly activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest user in the group

        if selected_user == 'overall':
            st.title('Most Busy User')
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WORD CLOUD
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


    # most common words
    most_common_df = helper.most_common_words(selected_user, df)

    fig,ax = plt.subplots()
    
    ax.barh(most_common_df[0], most_common_df[1])
    plt.xticks(rotation = 'vertical')
    st.title("Most Common Words")
    st.pyplot(fig)
