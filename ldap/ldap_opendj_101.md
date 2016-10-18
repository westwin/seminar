#### LDAP Introduction ####
##### LDAP Overview #####
- open industry standard, de facto access method for directory information.
- c/s based, TCP/IP is used.
- standard models:
    - Information Model
    - Naming Model
    - Functional Model
    - Security Model
    - ![four models](http://www.zytrax.com/books/ldap/ch2/ldap-stds-1.png)
    - LDAP does not define how data is stored, only how it is accessed. BUT most LDAP implementations do use a standard database as a back-end and indeed OpenLDAP offers a choice of back-end database support.
    - When you talk to an LDAP server you have no idea where the data comes from: in fact the whole point about the standard is to hide this level of detail. In theory the data may come from one OR MORE local databases or one OR MORE X.500 services (though these are about as rare as hen's teeth these days). Where and how you access the data is an implementation detail and is only important when you define the operational configuration of your LDAP server(s).
    - Keep the two concepts - access to the LDAP service and operation of the LDAP service - very clearly separate in your mind. When you design a directory based system figure out what you want it to do (the data organization) and forget the implementation. Then figure out as a second phase where the data is and how and where you want to store it - during LDAP operational configuration.
    - A number of commercial database products provide an LDAP view (an LDAP wrapper or an LDAP abstraction) of relational or other database types.
- LDAP vs Database ?
    - LDAP is characterized as a write once, read many-times service. not suitable for banking transaction. 
    - Read Optimized
    - LDAP has no transaction.([spring-ldap](http://docs.spring.io/spring-ldap/docs/1.3.x/reference/html/transactions.html) has a fake transaction impl.)
- LDAP Usage Summary

------
##### LDAP Schemas, ObjectClasses and Attributes #####
- When you create an entry in a DIT its data contents are contained in **attributes**, which are grouped into **objectclasses**, which are packaged into **schemas**.
- LDAP DIT Information(Data) Model, 
    - ![information model](http://www.zytrax.com/books/ldap/ch2/ldap-dit.png)
    - Each Entry is composed of one or more objectClass(es)
    - Each objectClass has a name and is a container for attrs
    - Each Attribute has a name, contains data, and is a member of one or more objectclass(es)
    - When the DIT is populated each entry will be uniquely identified(relative to its parent entry) in the herarchy by the data it contains.
- ObjectClasses
    - container for attributes.
    - each objectClass has a unique name.
    - the **objectclass** defines whether an attribute member **MUST** be present of **MAY** be present.
    - Each **objectclass** has a type which may be STRUCTURAL, AUXILLIARY or ABSTRACT. 
    - for each entry, there must be one and only one STRUCTURAL **objectclass**, but may be zero or more AUXILIARY **objectclass**
    - STRUCTURAL vs AUXILIARY vs ABSTRACT ?
    - [bunch of pre-defined `objectClass`(es)](http://www.zytrax.com/books/ldap/ape/), each of which contains lots of common `attributes`
- Attributes
    - All **attributes** are members of one, or more **objectclass(es)**
    - Each **attribute** defines the data type that it may contain.
    - **Attributes** may inherits all the characteristics of the parent attribute.
    - Each **attribute** has a unique name, and case-insensitive.
    - **attribute** can have *aliases* or *abbreviations*. For example, the `commonName` has an alias of `cn`.
    - **attribute** can be *single* or *multi* value.
      For example, it makes sense for a `person` to have multi `mail`, but one `userPassword`.
    - **attribute** can be unique.
    - **operational attributes**, for example,
        - **hasSubordinates** attr for `ou=People`, indicates if `ou=People` has any people entry
        - **numSubordinates** to indicates the # of how many people entry.
    - what is **dn** ?
        - the unique identifier for an entry in the DIT hierarchy
        - the sum of all `RDN`(s), see 
          ![dn desc](http://www.zytrax.com/books/ldap/ch2/dit-dn-rdn.png)
        - **dn** will be changed if an entry is moved from one parent to another parent. see `changetype: moddn`
        - uid=user.0,ou=People,dc=tenant1,dc=nqsky,dc=com

------
##### LDAP Operation #####
- ldapbind
- ldapsearch
    - Search Base
    - Search Scope
        - Object/Base: aka zero level, indicates a search of the base object only.
        - One Level: search the immediate suborniate
        - Subtree: search entire subree
    - Search Filter 
        - basic syntax
            - equals: `(attr=value)`
            - approximately equals: `(attr~=value)`
            - greater than: `(attr>=value)`
            - less than: `(attr<=value)`
            - wildcard: `\*` as a **presence** indicator
            - composite/combined filter,(looks like Reverse Polish Notation ?)
                - `(&(exp1)(exp2)(exp3))`: exp1 AND exp2 AND exp3
                - `(|(exp1)(exp2)(exp3))`: exp1 OR exp2 OR exp3
                - `(!(exp1))`: NOT exp1
                - `(&(!(exp1))(!(exp2)))`: NOT exp1 AND NOT exp2
        - sample filter/tips:
            - `(mail=*)`: returns all entries which have a `mail` attr.
            - `(objectclass=*)`: returns all entries.
            - `(mail=*@*)`: return entries with any valid RFC822 mail address.
            - `(objectclass=person)`: return entries which use `person` objectclass
    - best practice for **`ldap heartbeat query`**:
        - search filter uses `(objectclass=*)`
        - specify query returned attr is : String ATTR_NO_ATTRIBUTES = "1.1", see [rfc2251](http://www.rfc-editor.org/rfc/rfc2251.txt)

        > If the client does not want any attributes returned, it can specify
        > a list containing only the attribute with OID "1.1".  This OID was
        > chosen arbitrarily and does not correspond to any attribute in use.

    - **sepcial attrbitues**
        - If ldapsearch finds one or more entries, the attributes specified by attrs are returned.
        - If `*` is listed, all user attributes are returned. 
        - If `+` is listed, all operational attributes are returned. 
        - If only `1.1` is listed, no attributes will be returned. normally used for heartbeat/presence query.(for example, query if a user exists or not.)
        - If no attrs are listed, all user attributes are returned. (depends on ldapsearch impl)

    - ldap search pagination
        - ldap pagination control
        - count limit settings
        - ldap search `virtual list view index`, aka `vlv index`
      
- ldapmodify
    - changetype: moddn
        - newrdn
        - deleteoldrdn
    - changetype: modify
        - add
        - replace
        - delete

------
##### LDIF Overview #####
- Overview
- LDIF(LDAP Data Interchange Files) Format & Directives
    - LDIF are textual files that describe the tree hierarchy - DIT. And the data 
    - [LDIF Sample](http://www.zytrax.com/books/ldap/ch8/index.html)

------
##### LDAP Security #####
- Overview
    - Delegated Authentication Without the Security Risks of Password Synchronization
- TLS/SSL

-------
##### LDAP Refs #####
- [LDAP Glossary](http://www.zytrax.com/books/ldap/apd/)
- [LDAP - Object Classes and Attributes](http://www.zytrax.com/books/ldap/ape/)
- LDAP Browser: Apache Directory Studio, or JXplorer
- LDAP eBooks:
    - Understanding And Deploying Ldap Directory Services 2Nd
    - [LDAP for Rocket Scientists](http://www.zytrax.com/books/ldap/)

------
#### OpenDJ Introduction ####
##### Feature Overview #####
- LDAPv3-compliant directory service developed for Java
- HA, high-performance, secure store
- plenty of cmd tools and a full-featured `LDAP Java SDK`, plus `REST APIs`

------
##### Ease of Installation #####
- separate OpenDJ Software From Data, aka `instance.loc`
- silent install from command line
- set up data replication. (needs FQDN of each OpenDJ node. ip not working ??)

------
##### OpenDJ Refs #####
- [OpenDJ Home](https://backstage.forgerock.com)
- [OpenDJ Docs](https://backstage.forgerock.com/#!/docs/opendj/3)
    - [OpenDJ Administration Guide](https://backstage.forgerock.com/#!/docs/opendj/3/admin-guide)
    - [OpenDJ Configuration Reference](https://backstage.forgerock.com/static/docs/opendj/3/configref/)
    - [OpenDJ Installation Guide](https://backstage.forgerock.com/#!/docs/opendj/3/install-guide)
- [Get the Source Code](https://forgerock.org/projects/getting-the-source-code/)
    - Build from Source Code with Maven, `git clone` && `mvn clean install`
- [opendj-backends-and-multi-tenant-services](https://ludopoitou.com/2014/02/04/opendj-backends-and-multi-tenant-services/)

------
##### Home Work #####
- setup an ldap server
- install an ldap browser
- create some ldap entries
- do some basic ldap search
- define a new schema(attribute/objectclass) with some schema editor tool
- how to store user's password in ldap ? 
- **think how to design multi-tenancy**
- further reading 

------
##### What's Next ? #####
- study other `IDM` products. (okata ? OpenIDM ?)
- multi-tenancy design thoughts
    - each tenant has its own basedn for centralized storage/management.(in a single backend)
    - or we can separate each tenant in a separate backend. (for a large tenant...)
        - study OpenDJ backend for a better multi-tenancy design.
- data model
    - basic user profile, use ldap standard attr.
    - opendj specific attr
    - nqsky extended schema.
- integration with EMM
    - study EMM user/group data model 
    - setup a windows ad, then study its data model.
    - API def, CRUD on
        - Tenant
        - People
        - Group
        - Device ?
        - App ?
- authentication/authorization
