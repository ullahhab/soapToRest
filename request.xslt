<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:bank="http://example.com/bank"
    exclude-result-prefixes="bank">

    <!-- Identity template -->
    <xsl:output method="xml" indent="yes"/>

    <!-- Root template -->
    <xsl:template match="/bank:BankTransactionResponse">
        <TransformedResponse>
            <!-- Copy attributes -->
            <ResponseId><xsl:value-of select="@responseId"/></ResponseId>
            <RequestId><xsl:value-of select="@requestId"/></RequestId>
            <Timestamp><xsl:value-of select="@timestamp"/></Timestamp>

            <!-- Status -->
            <Status>
                <Code><xsl:value-of select="bank:Status/@code"/></Code>
                <Message><xsl:value-of select="bank:Status/@message"/></Message>
            </Status>

            <!-- Customer info -->
            <Customer>
                <CustomerId><xsl:value-of select="bank:Customer/bank:CustomerId"/></CustomerId>

                <Accounts>
                    <xsl:for-each select="bank:Customer/bank:AccountsSummary/bank:Account">
                        <Account>
                            <Type><xsl:value-of select="@type"/></Type>
                            <Currency><xsl:value-of select="@currency"/></Currency>
                            <AccountNumber><xsl:value-of select="bank:AccountNumber"/></AccountNumber>
                            <Balance><xsl:value-of select="bank:Balance"/></Balance>
                            <LastTransaction>
                                <TransactionId><xsl:value-of select="bank:LastTransaction/bank:TransactionId"/></TransactionId>
                                <Status><xsl:value-of select="bank:LastTransaction/bank:Status"/></Status>
                            </LastTransaction>
                        </Account>
                    </xsl:for-each>
                </Accounts>
            </Customer>

            <!-- Processed transactions -->
            <ProcessedTransactions>
                <xsl:for-each select="bank:ProcessedTransactions/bank:Transaction">
                    <Transaction>
                        <TransactionId><xsl:value-of select="@id"/></TransactionId>
                        <Status><xsl:value-of select="bank:Status"/></Status>
                        <ScheduledDate><xsl:value-of select="bank:ScheduledDate"/></ScheduledDate>
                    </Transaction>
                </xsl:for-each>
            </ProcessedTransactions>
        </TransformedResponse>
    </xsl:template>

</xsl:stylesheet>