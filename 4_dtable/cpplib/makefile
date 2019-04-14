NAME=example
CXX=g++
OFLAGS=-O3
CFLAGS=$(OFLAGS) -shared -fPIC
OBJS=example.o

%.o: %.cpp
	$(CXX) $(CFLAGS) -c $<

all: $(OBJS)
	$(CXX) $(CFLAGS) $(OBJS) -o $(NAME).so

clean:
	rm *.o $(NAME).so
