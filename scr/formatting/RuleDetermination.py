import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import statsmodels.api as sm

classification = [
    "Index",
    "Fatalities",
    "Crew",
    "Crew Fatalities",
    "Passengers",
    "Passengers Fatalities",
    "Total Fatalities",
]

data = pd.read_csv('Formated.csv')
classification_data = data[classification]

X = classification_data.drop(['Fatalities'], axis=1)
y = classification_data['Fatalities']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

reg = LogisticRegression()
reg.fit(X_train_scaled, y_train)

y_pred = reg.predict(X_test_scaled)

f1 = f1_score(y_test, y_pred, average='micro')
print(f1)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

sns.regplot(x=X_test['Index'], y=y_test, ax=ax1, scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'})
ax1.set_title('Initial Data')

sns.regplot(x=X_test['Index'], y=y_pred, ax=ax2, scatter_kws={'alpha': 0.5}, line_kws={'color': 'green'})
ax2.set_title('Predicted Data')

plt.tight_layout()
plt.show()
